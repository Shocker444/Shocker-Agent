# Deployment Guide to Vercel & Railway

This application uses a hybrid architecture:
1.  **Backend (Python/FastAPI)**: Handles WebSocket connections for real-time audio.
2.  **Frontend (Svelte)**: Connects to the backend via WebSockets.

Because Vercel Serverless Functions do not support long-lived WebSocket connections, **you cannot deploy the backend to Vercel**. Instead, we recommend deploying the Backend to **Railway** or **Render**, and the Frontend to **Vercel**.

---

## Part 1: Deploy Backend (Railway)

We recommend [Railway](https://railway.app/) as it automatically detects the configuration and supports persistent WebSocket connections.

1.  **Push your code to GitHub**.
2.  Sign up for **Railway**.
3.  Click **New Project** -> **Deploy from GitHub repo**.
4.  Select your repository.
5.  **Configure Environment Variables**:
    *   `DEEPGRAM_API_KEY`: Your Deepgram API Key.
    *   `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`): Your LLM API Key.
6.  **Build Command**: Railway should auto-detect the `Dockerfile` or `poetry.lock`. Ensure it uses the Dockerfile for best results.
7.  **Watch the deployment**. Once successful, Railway will give you a public URL (e.g., `https://shocker-agent-production.up.railway.app`).

**Note:** You need the `wss://` version of this URL for the frontend. (e.g., `wss://shocker-agent-production.up.railway.app/ws`).

---

## Part 2: Deploy Frontend (Vercel)

Now that your backend is running, deploy the frontend.

1.  Sign up for **Vercel**.
2.  Click **Add New Project** and import your GitHub repository.
3.  **Configure Project Settings**:
    *   **Root Directory**: Click "Edit" and change it to `web`.
    *   **Framework Preset**: Select "Vite".
    *   **Build Command**: `npm run build` (Default).
    *   **Output Directory**: `dist` (Default).
4.  **Environment Variables**:
    *   Add a new variable named `VITE_WS_URL`.
    *   Value: The WebSocket URL of your backend (e.g., `wss://shocker-agent-production.up.railway.app/ws`).
5.  Click **Deploy**.

---

## Verification

1.  Open your Vercel deployment URL.
2.  Open the browser console (F12).
3.  Check if you see "WebSocket connected".
4.  Try speaking! If configured correctly, you should see the visualizer react and hear the AI respond.
