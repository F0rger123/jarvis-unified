# 🤖 Jarvis Unified v2 - Complete Setup Guide

**100% FREE, modular AI assistant with all requested features**

---

## ✅ What's Included (All Free!)

| Feature | Status | Free? |
|---------|--------|-------|
| AI Chat (Ollama/Gemini/OpenRouter) | ✅ | YES - Ollama is 100% free |
| Voice TTS/STT | ✅ | pyttsx3 is FREE |
| Custom Tone (humorous/sassy/etc) | ✅ | YES |
| Wake Commands | ✅ | YES |
| Google Calendar | ✅ | YES (OAuth) |
| Gmail Integration | ✅ | YES (OAuth) |
| To-Do List | ✅ | YES |
| Screen Share Toggle | ✅ | YES (on-demand) |
| Gesture Learning | ✅ | YES |
| Browser Control (Chrome/Edge) | ✅ | YES |
| Automated Emails | ✅ | YES |
| GitHub Commit Summary | ✅ | YES |
| Mobile-Friendly UI | ✅ | YES |
| Theme Customization | ✅ | YES |
| Speech Visual Display | ✅ | YES |
| Memory & Preferences | ✅ | YES |

---

## 🚀 Quick Setup (15 minutes)

### 1. Clone
```bash
git clone https://github.com/F0rger123/jarvis-unified.git
cd jarvis-unified
```

### 2. Install
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r jarvis/requirements.txt
```

### 3. Configure for 100% FREE
```bash
cp jarvis/.env.example jarvis/.env

# EDIT .env - for completely FREE usage:
# 
# 1. Install Ollama (https://ollama.com)
# 2. Run: ollama serve  
# 3. Run: ollama pull qwen3:8b
# 4. In .env set:
#    AI_PROVIDER=ollama
#    OLLAMA_MODEL=qwen3:8b
# 
# Leave other API keys EMPTY for 100% free mode!
```

### 4. Run
```bash
python jarvis/main.py --web
```

### 5. Open Browser
```
http://localhost:5000
```

---

## 🎛️ Features Guide

### 🎤 Voice Setup
```bash
# Install voice dependencies
pip install pyttsx3 pyaudio

# In .env:
TTS_ENGINE=pyttsx3
STT_ENGINE=whisper
WAKE_WORD=Jarvis
CUSTOM_WAKE_COMMANDS=Hey Jarvis,Computer,Assistant
```

### 🎨 Customize Tone
In `.env`:
```bash
JARVIS_TONE=humorous   # funny, adds jokes
JARVIS_TONE=sassy     # direct, witty
JARVIS_TONE=formal    # professional
JARVIS_TONE=friendly  # warm
```

### 🎯 Customize UI
```bash
THEME=dark        # or light
ACCENT_COLOR=#3b82f6  # any hex color
SHOW_SPEECH_VISUAL=true
```

### 📅 Google Calendar/Gmail
1. Go to https://console.cloud.google.com
2. Create project → Enable Gmail API, Calendar API, Drive API
3. Create OAuth credentials (Web application)
4. Get Client ID + Secret → put in .env
5. Get refresh token (see docs/google-oauth.md)
6. Put refresh token in .env

### 🌐 Browser Control
```bash
DEFAULT_BROWSER=chrome  # chrome, edge, firefox
```

### 👋 Gesture Learning
Teach Jarvis hand gestures via the UI (Settings → Gestures)
- "Wave left" → "previous window"
- "Thumbs up" → "confirm"

### 📺 Screen Share
Toggle in UI - only activates when you turn it on (privacy!)

### ⚡ Automations
```bash
AUTO_EMAILS=true
EMAIL_SCHEDULE=07:00,19:00
```

### 📊 GitHub Integration
```bash
GITHUB_REPO=yourusername/yourrepo
GITHUB_TOKEN=ghp_xxx
```

---

## 📱 Mobile UI Features

- **Swipe-friendly** - Works great on phone
- **Theme toggle** - Dark/Light mode
- **Color picker** - Customize accent color
- **Speech visual** - See Jarvis "thinking"
- **Quick actions** - Tasks, Calendar, Auto, Gestures

---

## 💰 Cost Breakdown

| Component | Cost |
|-----------|------|
| Ollama (local AI) | **$0** |
| pyttsx3 (TTS) | **$0** |
| Whisper (STT) | **$0** |
| Google APIs | **$0** (free tier) |
| GitHub Actions | **$0** (2000 min/mo) |
| **TOTAL** | **$0/month** |

---

## 🆘 Troubleshooting

### "No AI provider"
- Install Ollama: https://ollama.com
- Run: `ollama serve`
- Run: `ollama pull qwen3:8b`

### Voice not working
- Linux: `sudo apt install espeak portaudio19-dev`
- Windows: usually works automatically
- Mac: `brew install portaudio`

### Google not working
- Need Client ID + Secret + Refresh Token
- See docs/google-oauth.md for full walkthrough

---

## 📁 File Structure

```
jarvis-unified/
├── jarvis/
│   ├── core/         # AI engine, config
│   ├── memory/       # Learning, todos, gestures
│   ├── voice/        # TTS/STT
│   ├── automation/   # Browser, files, gestures
│   ├── api/          # Google services
│   ├── ui/           # Web dashboard
│   ├── main.py       # Entry point
│   ├── .env.example  # Config template
│   └── SETUP.md      # This guide
├── requirements.txt
└── README.md
```

---

## ✅ What's Confirmed Free

- [x] Ollama + local models = 100% free forever
- [x] pyttsx3 TTS = free offline
- [x] Whisper STT = free local
- [x] Google APIs = free tier
- [x] All features included
- [x] Mobile-friendly UI
- [x] Cross-device control

**Version:** 2.0  
**Built:** April 2026  
**Goal:** 100% free, fully featured AI assistant