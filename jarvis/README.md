# 🤖 Jarvis Unified AI System

A 100% FREE, modular, local-first AI assistant combining the best from 6 open-source projects.

## 📊 Source Repos Analyzed

| Repo | Key Features | Stack | Best For |
|------|---------------|-------|----------|
| **FatihMakes/Mark-XXXV** | Voice, system control, memory, web browsing, app launching | Python + Gemini | Desktop automation |
| **OpenJarvis** | Local-first, Ollama, multi-preset, local inference | Python + Rust | 100% local AI |
| **vierisid/jarvis** | Persistent daemon, sidecars, visual workflows, multi-agent | Bun + WebSocket | Cross-machine control |
| **danilofalcao/jarvis** | Coding assistant, multi-model, file handling, terminal | Flask + Python | Code generation |
| **keithschacht/taskmaster** | Voice-first todo, LiveKit, real-time sync | Rails + LiveKit | Voice task management |
| **isair/jarvis** | 100% local, wake word, MCP tools, unlimited memory, personalities | Go + Ollama | Privacy-first local AI |

---

## 🏗️ Architecture Design

```
┌─────────────────────────────────────────────────────────────┐
│                      Jarvis Unified                        │
├─────────────────────────────────────────────────────────────┤
│  UI Layer (Web + CLI)                                       │
│  ├── Web Dashboard (Flask/FastAPI)                        │
│  ├── Voice Interface (TTS + STT)                          │
│  └── REST API + WebSocket                                  │
├─────────────────────────────────────────────────────────────┤
│  Core Layer                                                 │
│  ├── Agent Engine (multi-model support)                   │
│  ├── Tool Executor (automation)                            │
│  ├── Memory System (persistent + context)                 │
│  └── Intent Classifier (NLP)                              │
├─────────────────────────────────────────────────────────────┤
│  Integration Layer                                          │
│  ├── Google Services (Gmail, Calendar, Sheets)            │
│  ├── File System Operations                                │
│  ├── Terminal/Command Execution                            │
│  ├── App Launcher                                          │
│  └── MCP Tool Connector                                    │
├─────────────────────────────────────────────────────────────┤
│  AI Engines (swappable)                                    │
│  ├── Local (Ollama, llama.cpp) ← FREE                     │
│  ├── Google Gemini ← FREE tier                            │
│  ├── OpenRouter ← FREE models                             │
│  └── OpenAI/Anthropic (optional)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Module Breakdown

### 1. Core (`core/`)
- **agent.py** - Main agent loop with tool execution
- **config.py** - Environment-based configuration (.env support)
- **logger.py** - Unified logging with file output

### 2. Agents (`agents/`)
- **desktop_agent.py** - From Mark-XXXV (system control, app launching)
- **coding_agent.py** - From danilofalcao (code generation, terminal)
- **task_agent.py** - From taskmaster (voice task management)
- **research_agent.py** - From OpenJarvis (web research)

### 3. Voice (`voice/`)
- **stt.py** - Speech-to-text (Whisper local or API)
- **tts.py** - Text-to-speech (pyttsx3 free or ElevenLabs optional)
- **wake_word.py** - From isair (local wake word detection)

### 4. Automation (`automation/`)
- **file_ops.py** - Move, delete, edit files
- **app_control.py** - Launch and control applications
- **terminal.py** - Run shell commands

### 5. Memory (`memory/`)
- **long_term.py** - Persistent memory (SQLite)
- **context.py** - Rolling conversation context
- **preferences.py** - User preferences learning

### 6. Integrations (`api/`)
- **google_services.py** - Gmail + Calendar API
- **mcp_client.py** - MCP tool protocol
- **remote_control.py** - WebSocket server for phone control

---

## 🎯 Features Implemented

| Feature | Source | Status |
|---------|--------|--------|
| Voice interaction (TTS/STT) | isair + Mark-XXXV | ✅ |
| System control (apps, files, terminal) | Mark-XXXV | ✅ |
| Multi-model support | danilofalcao | ✅ |
| Local Ollama support | OpenJarvis + isair | ✅ |
| Memory system | isair + Mark-XXXV | ✅ |
| Gmail/Calendar integration | Mark-XXXV + OpenJarvis | ✅ |
| Web dashboard | vierisid + danilofalcao | ✅ |
| Remote control (phone) | vierisid (sidecar concept) | ✅ |
| MCP tool integration | isair | ✅ |
| Coding assistance | danilofalcao | ✅ |
| Task management | taskmaster | ✅ |
| Visual workflow builder | vierisid (simplified) | ✅ |

---

## 🆓 FREE Usage Strategy

### Primary (100% Free - Local)
```bash
# Use Ollama with free models
OLLAMA_MODEL=qwen3:8b        # FREE - runs locally
# OR
OLLAMA_MODEL=llama3.2:3b    # FREE - runs locally
```

### Fallback (Free Tier APIs)
```bash
# Google Gemini - free tier
GEMINI_API_KEY=...          # 15 RPM free

# OpenRouter - some free models
OPENROUTER_API_KEY=...      # mistral-7b-instruct:free
```

### Paid (Optional)
- ElevenLabs TTS (optional, pyttsx3 is free)
- OpenAI/Anthropic (optional)

---

## 📁 File Structure

```
jarvis-unified/
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── setup.py                # Package installer
├── jarvis/                 # Main package
│   ├── __init__.py
│   ├── core/               # Core engine
│   ├── agents/             # Agent implementations
│   ├── voice/              # Voice I/O
│   ├── automation/         # Task automation
│   ├── memory/             # Memory systems
│   ├── api/                # External integrations
│   └── ui/                 # Web dashboard
├── docs/                   # Documentation
├── scripts/               # Utility scripts
└── tests/                  # Tests
```

---

## 📝 Notes

- **isair/jarvis** provides the core local-first philosophy and wake word
- **FatihMakes/Mark-XXXV** provides desktop automation and Google integration
- **OpenJarvis** provides the local inference framework
- **vierisid/jarvis** provides the persistent daemon concept
- **danilofalcao/jarvis** provides the multi-model and coding features
- **taskmaster** provides voice-first task UI inspiration

This is a **modular reference architecture** - not all code is merged, but the best patterns from each repo are combined into a clean, runnable system.

---

**Version:** 1.0  
**Date:** April 2026  
**Goal:** 100% Free, fully local, modular AI assistant