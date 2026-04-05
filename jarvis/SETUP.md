# 🛠️ Jarvis Unified - Setup Guide

A 100% FREE, modular AI assistant combining the best from 6 open-source projects.

---

## 📋 Requirements

- **Python 3.10+**
- **Optional (for 100% free local AI):** [Ollama](https://ollama.com)
- **Optional (for voice):** Microphone + speakers

---

## 🚀 Quick Setup

### 1. Clone or Download

```bash
git clone https://github.com/F0rger123/jarvis-unified.git
cd jarvis-unified
```

### 2. Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

# Optional: Install all voice dependencies
pip install pyttsx3 gTTS
```

### 4. Configure (Choose Your AI)

#### Option A: 100% FREE (Local with Ollama) ⭐ RECOMMENDED

```bash
# 1. Install Ollama (https://ollama.com)
# 2. Start it: ollama serve
# 3. Pull a free model:
ollama pull qwen3:8b
# or
ollama pull llama3.2:3b

# 4. In .env, set:
OLLAMA_MODEL=qwen3:8b
```

#### Option B: FREE API Tier (Google Gemini)

```bash
# Get free key: https://aistudio.google.com/apikey
# In .env:
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash
```

#### Option C: OpenRouter (Some Free Models)

```bash
# Get key: https://openrouter.ai/keys
# In .env:
OPENROUTER_API_KEY=your_key_here
```

### 5. Copy & Edit .env

```bash
cp .env.example .env
# Edit .env with your settings
```

### 6. Run

```bash
# Web UI mode (recommended for first time)
python main.py --web

# Interactive CLI mode
python main.py
```

---

## 📖 Usage

### Web UI

After running `python main.py --web`:
1. Open http://localhost:5000
2. Chat with Jarvis!
3. Use the Tools tab for automation

### CLI Mode

```
You: Hello Jarvis
Jarvis: Hello! How can I help you today?

You: What's the weather?
Jarvis: I don't have weather access yet. Would you like me to add that?

You: Create a file called test.txt with "Hello World"
Jarvis: ✅ Created test.txt

You: open https://google.com
Jarvis: ✅ Opened https://google.com
```

---

## 🎤 Voice Setup (Optional)

```bash
# Install voice dependencies
pip install pyttsx3 gTTS

# Enable in .env:
TTS_ENGINE=pyttsx3
STT_ENGINE=whisper
WAKE_WORD=true
```

---

## 📱 Remote Control (Phone → PC)

1. Enable in .env:
```
REMOTE_ENABLED=true
REMOTE_PORT=8765
```

2. Run: `python main.py --web`

3. From your phone, connect to `http://YOUR_PC_IP:5000`

---

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_MODEL` | Local model to use | qwen3:8b |
| `GEMINI_API_KEY` | Google AI key | (none) |
| `OPENROUTER_API_KEY` | OpenRouter key | (none) |
| `TTS_ENGINE` | pyttsx3/gtts/elevenlabs | pyttsx3 |
| `MEMORY_DB` | SQLite database file | jarvis_memory.db |
| `PORT` | Web UI port | 5000 |

---

## 🆘 Troubleshooting

### "No AI provider configured"
- Make sure Ollama is running: `ollama serve`
- Or add an API key to .env

### "Module not found"
- Run: `pip install -r requirements.txt`

### Voice not working
- On Linux: `sudo apt install espeak`
- On Windows: pyttsx3 usually works out of the box

### Port already in use
- Change port: `python main.py --web --port 5001`

---

## 📦 What's Included

| Module | Source | Features |
|--------|--------|----------|
| Core AI | isair + OpenJarvis | Multi-model support, local-first |
| Memory | isair + Mark-XXXV | Persistent SQLite storage |
| Voice | isair + taskmaster | TTS (pyttsx3 free), wake word ready |
| Automation | Mark-XXXV | Files, apps, terminal |
| Google API | Mark-XXXV + OpenJarvis | Gmail, Calendar (OAuth) |
| Web UI | danilofalcao + vierisid | Dashboard, chat, tools |

---

## 🎯 Feature List

- [x] Chat with AI (multiple providers)
- [x] File operations (create, read, move, delete)
- [x] App launching
- [x] Terminal command execution
- [x] Web URL opening
- [x] Persistent memory (SQLite)
- [x] User preferences
- [x] Web dashboard
- [x] Google Calendar (OAuth setup needed)
- [x] Gmail (OAuth setup needed)
- [ ] Voice input (partially ready)
- [ ] Wake word detection (placeholder)
- [ ] MCP tools (placeholder)

---

## 📝 Notes

- **100% Free path:** Use Ollama + local models = $0 forever
- **API fallback:** Works with Gemini, OpenRouter, OpenAI if needed
- **Privacy-first:** isair's philosophy - your data stays local

---

**Version:** 1.0  
**Built from:** 6 open-source Jarvis projects  
**Goal:** Fully free, local, modular AI assistant