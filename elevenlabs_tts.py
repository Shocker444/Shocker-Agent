import asyncio

from typing import AsyncIterator, Optional
import contextlib
import json
from urllib.parse import urlencode
from loguru import logger

import websockets
from websockets.client import WebSocketClientProtocol

from settings import settings

from events import TTSChunkEvent


class ElevenLabsTTS:
    def __init__(self,
                voice_id = "JBFqnCBsd6RMkjVDRZzb",
                stability = 0.5,
    ):
        self.voice_id = voice_id
        self.ws: WebSocketClientProtocol = None
        self._connection_signal = asyncio.Event()
        self._close_signal = asyncio.Event()

        self.api_key = settings.ELEVENLABS_API_KEY
        if not self.api_key:
            raise ValueError("ElevenLabs API key not set in settings.ELEVENLABS_API_KEY")

    async def receive_events(self) -> AsyncIterator[TTSChunkEvent]:
        while not self._close_signal.is_set():
            _, pending = await asyncio.wait([
                asyncio.create_task(self.close_signal.wait()),
                asyncio.create_task(self._connection_signal.wait())
            ],
            
            return_when=asyncio.FIRST_COMPLETED)

            with contextlib.suppress(asyncio.CancelledError):
                for task in pending:
                    task.cancel()
            
            if self._close_signal.is_set():
                break

            if self.ws and self.ws.close_code is None:
                self._connection_signal.clear()

                try:
                    async for raw_message in self.ws:
                        if isinstance(raw_message, bytes):
                            logger.info(f"ElevenLabs received bytes: {raw_message}")

                        else:
                            logger.info(f"ElevenLabs received message: {raw_message}")

                except websockets.exceptions.ConnectionClosed:
                    logger.info("ElevenLabs: Websocket connection closed.")

    async def send_text(self, text_output: str):
        ws = await self._ensure_connection()

        payload = {
            "text": text,
            "try_trigger_generation": self.trigger_generation,
            "flush": True
        }

        await ws.send(json.dumps(payload))

    async def close(self):
        if self._ws and self._ws.close_code is None:
            await self._ws.close()

        self._ws = None
        self._close_signal.is_set()
    
    async def _ensure_connection(self) -> WebSocketClientProtocol:
        if self._close_signal.is_set():
            raise RuntimeError("ElevenLabsTTS tried establishing a connection after it was closed")

        if self.ws and self.ws.close_code is None:
            return self.ws

        params = {
            "model":"eleven_multilingual_v2",
            "output_format": "pcm_24000",
            "language": "en-US"
        }

        url = f"wss://api/elevenlabs.io/text-to-speech/{self.voice_id}/stream_input?{urlencode(params)}"

        bos_message = {
            "text": " ",
            "voice_settings": {
                "stability": self.stability,
                "similarity": self.similarity
            },
            "xi_api_key": self.api_key
        }

        await self._ws.send(json.dumps(bos_message))

        self._connection_signal.is_set()

        return self._ws
