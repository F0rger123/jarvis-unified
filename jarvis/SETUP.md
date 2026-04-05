# 🤖 Jarvis Unified v3 - Complete Setup Guide

**100% FREE - Tron UI + Food Agent + Self-Learning + SMS + Brain Viz**

---

## ✅ All Features Included

| Feature | Status | Free? |
|---------|--------|-------|
| **Tron-Style UI** | ✅ Futuristic cyberpunk | YES |
| **Voice + Text Input** | ✅ Seamless switching | YES |
| **Food Agent** | ✅ Grocery ordering, recipes, timers | YES |
| **Self-Learning** | ✅ Grades responses, improves | YES |
| **Brain Visualization** | ✅ See agent connections | YES |
| **Dashboard Analytics** | ✅ Tasks, stats, workflow | YES |
| **SMS via Gmail** | ✅ Free carrier gateway | YES |
| **Security Confirmations** | ✅ Explicit confirmations | YES |

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

### 3. Configure (100% FREE)
```bash
cp jarvis/.env.example jarvis/.env

# For 100% FREE:
# 1. Install Ollama: https://ollama.com
# 2. Run: ollama serve
# 3. Run: ollama pull qwen3:8b
# 4. In .env:
#    AI_PROVIDER=ollama
#    OLLAMA_MODEL=qwen3:8b
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

## 🎮 TRON UI Features

### Visual Style
- **Cyberpunk/Tron aesthetic** - Glowing cyan (#00ffff)
- **Scanline effect** - Retro-futuristic
- **Animated grid background**
- **Pulsing status indicators**

### Input Modes
```bash
# Toggle between voice and text
INPUT_MODE=text   # or voice

# In UI: Click the ⌨️/🎤 button to switch
```

### Mobile Support
- Fully responsive design
- Swipe-friendly navigation
- Touch-optimized buttons

---

## 🍔 Food Agent

### What It Does
1. **Grocery Ordering** - Add items to cart from Walmart/Instacart/DoorDash
2. **Recipe Lookup** - Get ingredients and step-by-step
3. **Cooking Timers** - Set timers for recipes

### Usage Examples
```
You: Order milk, eggs, bread
Jarvis: 📝 Added to Walmart cart:
• milk, eggs, bread

⚠️ CONFIRMATION REQUIRED: Proceed to checkout?

You: How to make pasta?
Jarvis: 🍳 Pasta Recipe:
• Ingredients: pasta, sauce, cheese
• Steps: 3 | Time: 20 min

You: Set timer for 10 minutes
Jarvis: ⏱️ Timer set for 10 minutes!
```

### Security
- **Always confirms** before any order
- **CONFIRM_ORDERS=true** in config
- Shows items and store before checkout

---

## 🧠 Self-Learning System

### How It Works
1. Every response is logged
2. You can grade responses 1-5
3. Jarvis analyzes patterns
4. Improves system prompt over time

### Usage
```
# After each response, grade buttons appear:
[1] [2] [3] [4] [5]

# Jarvis tracks:
- Total responses
- Average grade
- Trend (improving/declining)
- Pattern suggestions
```

### Stats
View in dashboard - shows your grading history and Jarvis's learning progress!

---

## 🧠 Brain Visualization

### What You See
- All active agents and their connections
- Real-time workflow visualization
- Node interactions

### Agents Displayed
```
CORE → MEMORY → LEARNING
  ↓       ↓        ↓
VOICE → FOOD → GOOGLE
  ↓       ↓        ↓
BROWSER → SMS → CALENDAR
```

---

## 📊 Dashboard

### Stats Shown
- **Tasks** - Pending vs completed
- **Learning** - Grade average, trend
- **Brain** - Active nodes, connections
- **Agents** - How many running

---

## 📱 SMS via Gmail (FREE)

### How It Works
- Uses carrier email gateways (free)
- verizon → @vtext.com
- att → @txt.att.net
- tmobile → @tmomail.net
- sprint → @messaging.sprintpcs.com

### Security
- **CONFIRM_SMS=true** (default)
- Always asks before sending
- Shows preview before confirm

### Example
```
You: Send text to mom "Call me"
Jarvis: ⚠️ CONFIRMATION REQUIRED:
Send SMS to mom:
"Call me"

Reply 'yes' to confirm
```

---

## 🔒 Security Features

All sensitive actions require explicit confirmation:

| Action | Default | Setting |
|--------|---------|---------|
| Payments | Confirm | CONFIRM_PAYMENTS=true |
| Orders | Confirm | CONFIRM_ORDERS=true |
| SMS | Confirm | CONFIRM_SMS=true |

---

## ⚡ Automations

### Available
- Daily email summaries
- GitHub commit summaries
- Calendar event reminders
- Task management

### Config
```bash
AUTO_EMAILS=true
EMAIL_SCHEDULE=07:00,19:00
GITHUB_REPO=username/repo
```

---

## 💰 Cost: $0/Month

| Component | Cost |
|-----------|------|
| Ollama (local AI) | **$0** |
| pyttsx3 (TTS) | **$0** |
| SMS via Gmail | **$0** |
| Brain Viz | **$0** |
| All Features | **$0** |

---

## 🎛️ Configuration

### UI Theme
```bash
UI_THEME=tron
ACCENT_COLOR=#00ffff
GRID_COLOR=#00ffff33
```

### Tone
```bash
JARVIS_TONE=humorous  # or sassy, formal, friendly
```

### Learning
```bash
SELF_LEARNING=true
LEARNING_DB=jarvis_learning.json
```

---

## 📱 Mobile Features

- Responsive Tron design
- Touch-optimized controls
- Voice input button
- Swipe navigation

---

## 🆘 Troubleshooting

### "Food order not working"
- Food agent is simulated - shows what would be ordered
- Real ordering needs API keys for Walmart/Instacart

### "SMS not sending"
- Needs Google OAuth setup
- Or use carrier email gateway manually

### "Brain viz not showing"
- Check BRAIN_VIZ=true in config

---

## 📁 File Structure

```
jarvis-unified/
├── jarvis/
│   ├── core/         # AI + Learning + Config
│   ├── memory/       # Tasks + preferences
│   ├── voice/       # TTS/STT
│   ├── automation/   # Browser, gestures
│   ├── api/          # Google + SMS
│   ├── ui/           # Tron UI
│   ├── main.py
│   ├── .env.example
│   └── SETUP.md
└── README.md
```

---

**Version:** 3.0  
**Date:** April 2026  
**Goal:** 100% free, fully featured, beautiful AI assistant

**SECURITY:** All payments/orders/SMS require explicit confirmation by default!