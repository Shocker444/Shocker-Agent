# Shocker Agent ⚡

Shocker Agent is an advanced AI-powered Talent Acquisition Specialist and Technical Interviewer. It conducts structured, competency-based voice interviews based on provided Job Descriptions (JD).

Built with a modern real-time architecture, it features low-latency voice interaction using Deepgram (STT & TTS), intelligent conversation management with LangChain/LangGraph, and a reactive Svelte frontend with real-time audio visualization.

## 🚀 Features

- **Voice-First Interface**: Real-time, full-duplex voice conversation with the AI agent.
- **AI Interviewer Persona**: "Shocker" conducts professional technical screenings, adapts to candidate responses, and follows a structured interview protocol.
- **Real-time Audio Pipeline**: Powered by Deepgram for ultra-fast Speech-to-Text and Text-to-Speech.
- **Dynamic Questioning**: Generates questions based on the specific Job Description provided.
- **Reactive UI**: Svelte-based frontend with real-time audio visualization and activity feed.
- **Event-Driven Architecture**: WebSocket-based communication handling audio streams and agent events.

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** (WebSockets & API)
- **LangChain & LangGraph** (Agent Logic)
- **Deepgram SDK** (STT & TTS)
- **Poetry** (Dependency Management)

### Frontend
- **Svelte 5**
- **TypeScript**
- **Vite**
- **TailwindCSS**

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js & npm
- [Poetry](https://python-poetry.org/) (for Python dependency management)
- API Keys for:
  - [Deepgram](https://deepgram.com/)
  - OpenAI or Anthropic (depending on the configured LLM)

## 📦 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd Shocker-Agent
```

### 2. Backend Setup
Install the Python dependencies using Poetry:
```bash
poetry install
```

Create a `.env` file in the root directory and add your API keys:
```ini
DEEPGRAM_API_KEY=your_deepgram_key
OPENAI_API_KEY=your_openai_key
# or ANTHROPIC_API_KEY=your_anthropic_key
```

### 3. Frontend Setup
Navigate to the web directory and install dependencies:
```bash
cd web
npm install
```

## 🏃‍♂️ Usage

### Start the Backend
From the root directory:
```bash
poetry run python main.py
```
The server will start at `http://0.0.0.0:8000`.

### Start the Frontend
In a new terminal, navigate to the `web` directory:
```bash
cd web
npm run dev
```
Open your browser and navigate to the local URL provided by Vite (usually `http://localhost:5173`).

## 📂 Project Structure

```
Shocker-Agent/
├── main.py              # Application entry point & WebSocket handler
├── agent.py             # LangGraph agent definition
├── prompts.py           # System prompts & TTS guidelines
├── deepgram_stt.py      # Deepgram integration (STT/TTS)
├── events.py            # Event definitions for the pipeline
├── misc/                # Miscellaneous files (e.g., sample JDs)
├── pyproject.toml       # Python dependencies
├── web/                 # Svelte Frontend
│   ├── src/
│   │   ├── App.svelte       # Main component
│   │   ├── lib/
│   │   │   ├── components/  # UI Components (Visualizer, Controls, etc.)
│   │   │   ├── audio/       # Audio capture & playback logic
│   │   │   ├── websocket.ts # WebSocket client logic
│   │   │   └── stores/      # Svelte stores
│   └── package.json
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[MIT](LICENSE)
