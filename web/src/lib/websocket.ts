import type { ServerEvent } from "./types";
import {
    session,
    currentTurn,
    latencyStats,
    waterfallData,
    activities,
    logs
} from "./stores";

import { createAudioCapture, createAudioPlayback } from "./audio";
import { get } from "svelte/store";

export interface VoiceSession {
    start: () => Promise<void>;
    stop: () => void;
}

export function createVoiceSession(): VoiceSession {
    let ws: WebSocket | null = null;
    let ttsFinishTimeout: ReturnType<typeof setTimeout> | null = null;


    const audioCapture = createAudioCapture()
    const audioPlayback = createAudioPlayback()

    function handleEvent(event: ServerEvent) {
        const turn = get(currentTurn);
        console.log("Handling event:", event.type);
        switch (event.type) {
            case "stt_chunk":
                if (!turn.active) {
                    const prevTurn = get(currentTurn);
                    if (prevTurn.turnStartTs) {
                        waterfallData.set({ ...prevTurn });
                    }
                    currentTurn.startTurn(event.timestamp);
                }
                currentTurn.sttStart(event.timestamp);
                currentTurn.sttChunk(event.text);
                break;

            case "stt_output":
                currentTurn.sttEnd(event.timestamp, event.text);
                activities.add("stt", "Transcription", event.text);
                break;

            case "agent_chunk":
                currentTurn.agentChunk(event.timestamp, event.text);
                break;

            case "agent_end":
                currentTurn.agentEnd(event.timestamp, event.text);
                activities.add("agent", "Agent Response", event.text);
                break;

            case "tool_call":
                activities.add(
                    "tool",
                    `Tool called: ${event.tool_name}`,
                    "Called with arguments:",
                    event.args
                );
                logs.log(`Tool call: ${event.tool_name}`);
                break;

            case "tool_return":
                activities.add(
                    "tool",
                    `Tool: ${event.tool_name}`,
                    "Called with arguments:",
                    event.args
                );
                logs.log(`Tool call: ${event.tool_name}`);
                break;

            case "tts_chunk":
                const currentTurnstate = get(currentTurn)
                if (!currentTurnstate.ttsStartTs && currentTurnstate.response) {
                    activities.add("agent", "Agent Response", currentTurnstate.response);
                }
                currentTurn.ttsChunk(event.timestamp)
                audioPlayback.push(event.audio)

                if (ttsFinishTimeout) clearTimeout(ttsFinishTimeout);
                ttsFinishTimeout = setTimeout(() => {
                    const t = get(currentTurn);
                    if (t.active && t.sttEndTs && t.ttsEndTs) {
                        finishTurn();
                    }
                }, 300);
                break;

        }
    }



    function finishTurn() {
        const turn = get(currentTurn);
        waterfallData.set({ ...turn });
        latencyStats.recordTurn(turn);
        currentTurn.finishTurn();
    }

    async function start(): Promise<void> {

        session.reset();
        currentTurn.reset();
        latencyStats.reset();
        waterfallData.set(null);
        activities.clear();
        logs.clear();
        logs.clear();

        session.setStatus("connecting");

        // connect websocket
        ws = new WebSocket("ws://localhost:8000/ws");

        console.log("WebSocket connecting...", ws);


        ws.binaryType = "arraybuffer";

        console.log(ws.binaryType)

        ws.onopen = async () => {
            session.connect();
            logs.log("Session started.");
            console.log("WebSocket connected.");

            try {
                
                await audioCapture.start((chunk) => {
                    if (ws && ws.readyState == WebSocket.OPEN) {
                        ws.send(chunk);
                    }
                });
                logs.log("Audio capture started.");
                logs.log("Session started.");

            } catch (err) {
                console.error(err);
                logs.log(
                    `Error: ${err instanceof Error ? err.message : "Unknown error"}`
                );
                session.setStatus("error");
                stop();
            }
        };

        ws.onmessage = async (event) => {
            console.log("WebSocket message received:", event);
            const eventData: ServerEvent = JSON.parse(event.data)
            console.log("Parsed event data:", eventData);
            handleEvent(eventData);
        };

        ws.onclose = () => {
            session.disconnect();
            logs.log("WebSocket disconnected");
            console.log("websocket closed");
        };

        ws.onerror = (e) => {
            console.error(e);
            logs.log("WebSocket error");
            session.setStatus("error");
        };
    }

    function stop(): void {
        logs.log("Session ended");

        if (ttsFinishTimeout) {
            clearTimeout(ttsFinishTimeout);
            ttsFinishTimeout = null;
        }

        audioCapture.stop()
        audioPlayback.stop()

        if (ws) {
            ws.close();
            ws = null;
            console.log("WebSocket closed");
        }

        session.reset();
    }

    return { start, stop }

}
