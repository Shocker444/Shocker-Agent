import { writable, derived} from "svelte/store";
import type { SessionState } from "../types";

function createSessionStore() {
  const { subscribe, set, update } = writable<SessionState>({
    connected: false,
    recording: false,
    status: "ready",
    duration: null,
    remainingTime: null,
    startTime: null,
    elapsed: 0,
  });

  let timerInterval: ReturnType<typeof setInterval> | null = null;

  return {
    subscribe,

    connect(durationMins: number = 10) {
      const durationSeconds = durationMins * 60;
      update((s) => ({
        ...s,
        connected: true,
        recording: true,
        status: "listening",
        duration: durationSeconds,
        remainingTime: durationSeconds,
        startTime: Date.now(),
        elapsed: 0,
      }));
      // Start timer
      timerInterval = setInterval(() => {
        update((s) => {
          const elapsed = s.startTime
            ? Math.floor((Date.now() - s.startTime) / 1000)
            : 0;
          const remainingTime = s.duration
            ? s.duration - elapsed
            : null;

          // Auto-disconnect if session time is up
          if (remainingTime !== null && remainingTime <= 0) {
            if (timerInterval) {
              clearInterval(timerInterval);
              timerInterval = null;
            }
            return {
              ...s,
              elapsed,
              remainingTime: 0,
              connected: false,
              recording: false,
              status: "disconnected",
            };
          }

          return {
            ...s,
            elapsed,
            remainingTime,
          };
        });
      }, 1000);
    },

    disconnect() {
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
      }
      update((s) => ({
        ...s,
        connected: false,
        recording: false,
        status: "disconnected",
      }));
    },

    setStatus(status: SessionState["status"]) {
      update((s) => ({ ...s, status }));
    },

    reset() {
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
      }
      set({
        connected: false,
        recording: false,
        status: "ready",
        duration: null,
        remainingTime: null,
        startTime: null,
        elapsed: 0,
      });
    },
  };
}

export const session = createSessionStore();

// Derived store for formatted time
export const formattedTime = derived(session, ($session) => {
  const timeDisplay = $session.remainingTime !== null 
    ? $session.remainingTime 
    : $session.elapsed;
  
  const safeTime = Math.max(0, timeDisplay);
  const mins = Math.floor(safeTime / 60);
  const secs = safeTime % 60;
  return `${mins}:${secs.toString().padStart(2, "0")}`;
});