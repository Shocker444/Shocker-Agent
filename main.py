import asyncio
import contextlib
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
from misc.sample_jd import Job_description
from settings import settings


from deepgram import DeepgramSTT, DeepgramTTS
from elevenlabs_tts import ElevenLabsTTS

from events import (
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


async def _stt_stream(
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
        event_count = 0
        async for event in stt.receive_events():
            #print(f"📥 Received STT event #{event_count}: {type(event).__name__}")  # ← ADD THIS
            #print(f"   Event details: {event}") 
            yield event
    
    finally:

        with contextlib.suppress(asyncio.CancelledError):
            send_task.cancel()
            await send_task

        await stt.close()



async def _agent_stream(
        event_stream: AsyncIterator[VoiceAgentEvent]
) -> AsyncIterator[VoiceAgentEvent]:
    '''
    Processes STT events through the agent and yields VoiceAgentEvents
    '''

    thread_id = str(uuid4())  # unique ID for this conversation thread
    async for event in event_stream:
        yield event

        
        if event.type == "stt_output":
            buffer = []
            stream = agent.astream(
                {"messages": [HumanMessage(content=event.text)], "job_description": Job_description},
                {"configurable": {"thread_id": thread_id}},
                stream_mode="messages",
                flush=True
            )
            async for message, metadata in stream:
                # logger.info(f"Agent Message: {message}")
                try:
                    if isinstance(message, AIMessage):
                        logger.info(f"Agent Response: {message.content}")
                        yield AgentChunkEvent(
                            text=message.content
                        )
                        buffer.append(message.content)
                except IndexError:
                    logger.error(f"IndexError: {message.content}")

            if buffer:
                yield AgentEndEvent(text="\n".join(buffer))


async def _tts_stream(
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

                    yield InterruptEvent()

                else:
                    pass

        except Exception as e:
            logger.error(f"Error while processing text: {e}")
            raise

    

    try:
        async for events in merge_async_iters(process_upstream(), tts.receive_events()):
            yield events

    finally:
        await tts.close()


    


pipeline = (RunnableGenerator(_stt_stream) | RunnableGenerator(_agent_stream) | RunnableGenerator(_tts_stream))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("✅ WebSocket client connected")
    await websocket.accept()
    logger.info("🤝 WebSocket accepted")

    async def websocket_audio_stream() -> AsyncIterator[bytes]:
        while True:
            try:
                data = await websocket.receive_bytes()
                yield data
            except WebSocketDisconnect:
                # This is expected! It means the user clicked "End Session"
                logger.info("Client disconnected gracefully")
                break  # Break the loop to stop processing
            except Exception as e:
                logger.error(f"Unexpected error receiving audio: {e}")
                break


    output_stream = pipeline.atransform(websocket_audio_stream())
    print(output_stream)

    async for event in output_stream:
        await websocket.send_json(event_to_dict(event))


# Mount static files (frontend)
'''if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
else:
    print(f"⚠️  Warning: Static directory not found at {STATIC_DIR}")
    print("Frontend will not be served. Build it with: npm run build")'''


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8000,
                reload=settings.is_development)