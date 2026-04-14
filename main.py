import asyncio
import contextlib
import json
import base64
import os
import tempfile
import io
#from pypdf import PdfReader
from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path
from typing import AsyncIterator
from uuid import uuid4
from loguru import logger

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableGenerator
from langgraph.checkpoint.memory import InMemorySaver
from agent import agent
from utils import merge_async_iters
#from misc.sample_jd import Job_description
from settings import settings


from deepgram import DeepgramSTT, DeepgramTTS
from elevenlabs_tts import ElevenLabsTTS

from events import (
    AgentTriggerEvent,
    AgentChunkEvent,
    AgentEndEvent,
    ToolCallEvent,
    ToolReturnEvent,
    VoiceAgentEvent,
    InterruptEvent,
    event_to_dict,
    )


'''STATIC_DIR = Path(__file__).parent/"web"/"dist"

if not STATIC_DIR.exists():
    raise RuntimeError("Static directory not found. Please build the web frontend before running the server.")'''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class VoicePipeline:
    def __init__(self, job_description: str, resume: str, duration: int, time_left: int):
        # Keeps track of whether this specific session has triggered the agent yet.
        # This prevents global state mutations that affect concurrent users.
        self.has_triggered = False
        self.job_description = job_description
        self.resume = resume
        self.duration = duration
        self.time_left = time_left

    async def _stt_stream(
            self,
            audio_stream: AsyncIterator[bytes],
        ) -> AsyncIterator[VoiceAgentEvent]:

        stt = DeepgramSTT()
        print("STT stream started")

        async def send_audio():
            """
            Background task that pumps audio chunks to Deepgram 
            """
            chunk_count = 0

            try:
                # Stream each audio chunk to deepgram as it arrives
                async for audio_chunk in audio_stream:
                    if isinstance(audio_chunk, bytes):
                        await stt.send_audio(audio_chunk)
                    elif isinstance(audio_chunk, str):
                        # Handle the text signal
                        pass
            finally:
                await asyncio.sleep(0.2)  # wait for any final events
                await stt.close()

        # launch the audio task in the background

        send_task = asyncio.create_task(send_audio())
        #print(f"🚀 Background audio task created: {send_task}")

        try:
            if settings.AGENT_TRIGGER and not self.has_triggered:
                yield AgentTriggerEvent(text="START")
                self.has_triggered = True

            async for event in stt.receive_events():
                yield event
        
        finally:

            with contextlib.suppress(asyncio.CancelledError):
                send_task.cancel()
                await send_task

            await stt.close()



    async def _agent_stream(
            self,
            event_stream: AsyncIterator[VoiceAgentEvent]
    ) -> AsyncIterator[VoiceAgentEvent]:
        '''
        Processes STT events through the agent and yields VoiceAgentEvents
        '''

        thread_id = str(uuid4())  # unique ID for this conversation thread
        async for event in event_stream:
            yield event

            
            if event.type == "stt_output" or event.type == "agent_trigger":
                buffer = []
                stream = agent.astream(
                    {"messages": [HumanMessage(content=event.text)],
                     "job_description": self.job_description,
                     "resume": self.resume,
                     "duration": self.duration,
                     "time_left": self.time_left},
                    {"configurable": {"thread_id": thread_id}},
                    stream_mode="messages",
                    flush=True
                )


                async for message, metadata in stream:
                    # logger.info(f"Agent Message: {message}")
                    try:
                        if isinstance(message, AIMessage):

                            yield AgentChunkEvent(
                                text=message.content
                            )
                            buffer.append(message.content)
                    except IndexError:
                        logger.error(f"IndexError: {message.content}")

                if buffer:
                    yield AgentEndEvent(text="".join(buffer))


    async def _tts_stream(
            self,
            event_stream: AsyncIterator[VoiceAgentEvent]
    ) -> AsyncIterator[VoiceAgentEvent]:
        
        tts = DeepgramTTS()

        async def process_upstream():

            try:
                async for event in event_stream:
                    yield event
                    if event.type == "agent_end":
                        await tts.send_text(event.text)
                        await tts.flush()

                    elif event.type == "stt_output":
                        # BARGE-IN: User is speaking, so we shut up.
                        # 1. Tell Deepgram to stop producing audio.
                        
                        # 2. Throw away any text we were about to speak.
                        if not settings.AGENT_TRIGGER or self.has_triggered:
                            await tts.clear()

                            yield InterruptEvent()

                    else:
                        pass

            except Exception as e:
                logger.error(f"Error while processing text: {e}")
                raise
            finally:
                await asyncio.sleep(0.2)
                await tts.close()

        

        try:
            async for events in merge_async_iters(process_upstream(), tts.receive_events()):
                yield events

        finally:
            await tts.close()

    def get_runnable(self):
        return (RunnableGenerator(self._stt_stream) | RunnableGenerator(self._agent_stream) | RunnableGenerator(self._tts_stream))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("✅ WebSocket client connected")
    await websocket.accept()
    logger.info("🤝 WebSocket accepted")

    async def websocket_audio_stream() -> AsyncIterator[bytes]:
        while True:
            try:
                message = await websocket.receive()
                if message.get("type") == "websocket.disconnect":
                    logger.info("Client disconnected gracefully")
                    break
                if "bytes" in message and message.get("bytes"):
                    yield message["bytes"]
                elif "text" in message and message.get("text"):
                    data = json.loads(message["text"])
                    if data.get("type") == "time_update":
                        voice_pipeline.duration = data.get("duration", voice_pipeline.duration)
                        voice_pipeline.time_left = data.get("time_left", voice_pipeline.time_left)
            except WebSocketDisconnect:
                # This is expected! It means the user clicked "End Session"
                logger.info("Client disconnected gracefully")
                break  # Break the loop to stop processing
            except RuntimeError as e:
                # Catch specific RuntimeErrors, although we've avoided it now
                logger.error(f"RuntimeError receiving audio: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error receiving audio: {e}")
                break

    data = await websocket.receive_json()
    logger.info(f"Received data keys: {list(data.keys())}")
    
    resume_text = "N/A"
    
    try:
        if "resume_base64" in data and data["resume_base64"]:
            pdf_bytes = base64.b64decode(data["resume_base64"])
            
            # PyMuPDFLoader expects a physical file path, not a streaming byte object.
            # We save it to a temporary system file, read it, and then delete it.
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_bytes)
                tmp_file_path = tmp_file.name

            try:
                loader = PyMuPDFLoader(tmp_file_path)
                docs = loader.load()
                resume_text = "\n".join(docs[i].page_content for i in range(len(docs)))
                logger.info("Successfully extracted resume text securely.")
            finally:
                # Always clean up the temporary file
                os.unlink(tmp_file_path)

    except Exception as e:
        logger.error(f"Failed to read resume PDF: {e}")
        resume_text = "N/A"

    voice_pipeline = VoicePipeline(
        data.get("job_description", ""), 
        resume=resume_text,
        duration=data.get("duration", 0), 
        time_left=data.get("time_left", 0)
    )
    
    output_stream = voice_pipeline.get_runnable().atransform(websocket_audio_stream())

    try:
        async for event in output_stream:
            await websocket.send_json(event_to_dict(event))
    finally:
        pass

if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8000,
                reload=settings.is_development)