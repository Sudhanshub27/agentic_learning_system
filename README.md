# 🧠 Agentic Learning System

An autonomous AI-powered learning system that adapts to each user's knowledge level and learning pace. Built with a multi-agent architecture, it can teach **any subject** — from Python to Constitutional Law — using an intelligent loop:

**PLAN → TEACH → TEST → ANALYZE → ADAPT → MEMORY UPDATE → REPEAT**

## ✨ Key Features

- **🤖 6 Specialized AI Agents**: Planner, Tutor, Evaluator, Analyzer, Strategy, Memory
- **🎯 Any Subject**: Dynamically generates curriculum for any domain (CS, Law, Medicine, Arts...)
- **📊 Adaptive Difficulty**: Automatically adjusts based on performance
- **🧠 Persistent Memory**: Tracks progress across sessions
- **🔀 Multi-LLM Smart Routing**: Uses 4 free LLM providers with automatic failover
- **⚡ Fully Autonomous**: System decides what to teach, when to test, and how to adapt

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│                  Frontend (Next.js)               │
├──────────────────────────────────────────────────┤
│                  API Layer (FastAPI)               │
├──────────────────────────────────────────────────┤
│              Orchestrator (LangGraph)              │
├──────┬──────┬──────┬──────┬──────┬───────────────┤
│Planner│Tutor│Eval  │Analyz│Strat │    Memory     │
├──────┴──────┴──────┴──────┴──────┴───────────────┤
│           LLM Providers (LiteLLM)                 │
│    Ollama │ Gemini │ Groq │ DeepSeek              │
├──────────────────────────────────────────────────┤
│         Storage (SQLite/PostgreSQL + ChromaDB)    │
└──────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.ai) installed with `llama3.2:3b` model
- (Optional) Free API keys for Gemini, Groq, DeepSeek

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/agentic-learning-system.git
cd agentic-learning-system

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
cd backend
pip install -e ".[dev]"

# Configure environment
cp ../.env.example ../.env
# Edit .env with your API keys

# Start Ollama (in another terminal)
ollama serve

# Run the server
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the Swagger UI.

## 🔑 LLM Providers (All Free)

| Provider | Setup | Used For |
|----------|-------|----------|
| Ollama | `ollama pull llama3.2:3b` | Primary (local, unlimited) |
| Gemini | [Get free key](https://aistudio.google.com/apikey) | Complex reasoning |
| Groq | [Get free key](https://console.groq.com/keys) | Fast grading |
| DeepSeek | [Get free key](https://platform.deepseek.com) | Coding tasks |

## 📁 Project Structure

```
backend/
├── app/
│   ├── agents/          # 6 specialized AI agents
│   ├── orchestrator/    # LangGraph state machine
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic validation
│   ├── services/        # LLM service, knowledge tracker
│   ├── api/             # FastAPI routes
│   ├── db/              # Database engine
│   ├── prompts/         # Agent prompt templates
│   ├── config.py        # Settings management
│   └── main.py          # FastAPI entry point
└── tests/               # pytest test suite
```

## 🛠️ Tech Stack

- **Backend**: Python + FastAPI
- **Agents**: LangGraph (graph-based orchestration)
- **LLM**: LiteLLM (multi-provider interface)
- **Database**: SQLAlchemy 2.0 (async) + SQLite/PostgreSQL
- **Vector Store**: ChromaDB
- **ML**: scikit-learn
- **Frontend**: Next.js + TypeScript (coming soon)

## 📄 License

MIT
