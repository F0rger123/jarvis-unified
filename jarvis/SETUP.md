# Jarvis Unified v3.2 - Setup Guide
# Gemini 3.1 Flash Lite + WhatsApp + Packaged

---

## 🚀 EASY SETUP (Download & Go!)

### Option 1: Quick Start (No Install)

1. **Get Gemini API Key (FREE)**
   - Go to: https://aistudio.google.com/app/apikey
   - Copy your API key

2. **Run the Setup Script**
   
   **Windows:**
   ```batch
   download_jarvis.bat
   ```
   
   **Mac/Linux:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Enter Your Keys When Prompted**
   - Gemini API Key
   - (Optional) WhatsApp credentials

4. **Open Browser**
   ```
   http://localhost:5000
   ```

---

## 📦 Package Contents

### What's Included
- ✅ Jarvis v3.2 (all features)
- ✅ Tron UI
- ✅ Gemini 3.1 Flash Lite integration
- ✅ WhatsApp setup UI
- ✅ Self-learning
- ✅ Food agent
- ✅ Dashboard

---

## 🔧 WhatsApp Setup (In-App!)

### Step 1: Open Jarvis in Browser
Go to http://localhost:5000

### Step 2: Go to Settings
Click the ⚙️ gear icon

### Step 3: WhatsApp Section
Find "WhatsApp Integration"

### Step 4: Choose Method

**Option A: Twilio (Easier)**
1. Go to https://console.twilio.com
2. Get a WhatsApp-enabled number
3. Copy: Account SID, Auth Token, Phone Number
4. Paste into Jarvis settings

**Option 2: WhatsApp Business API**
1. Go to https://developers.facebook.com/
2. Create app → WhatsApp
3. Get Phone ID and Access Token
4. Paste into Jarvis settings

### Step 5: Save & Test
Click "Save" then test with:
```
Send WhatsApp to [your number] "Hello from Jarvis!"
```

---

## 💰 Costs: $0

| Feature | Cost |
|---------|------|
| Gemini 3.1 Flash Lite | **FREE** (best free tier!) |
| Twilio (up to 1k msgs) | **$0** |
| Jarvis running locally | **$0** |
| **Total** | **FREE** |

---

## 📱 Device Support

### Works On:
- ✅ Windows PC
- ✅ Mac
- ✅ Linux
- ✅ Android phone
- ✅ iPhone
- ✅ Tablet
- ✅ Any device with browser!

### How to Access:
1. Start Jarvis on your computer
2. Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. On phone: `http://YOUR_PC_IP:5000`

---

## 🛠️ Manual Setup (If Package Doesn't Work)

```bash
# 1. Clone
git clone https://github.com/F0rger123/jarvis-unified.git

# 2. Install
cd jarvis-unified
pip install -r requirements.txt

# 3. Configure
cp jarvis/.env.example jarvis/.env
# Edit .env with your keys

# 4. Run
python jarvis/main.py --web
```

---

## 🔐 Security Confirmations

All sensitive actions require "yes" to confirm:
- 💳 Payments
- 🛒 Orders
- 📱 WhatsApp messages
- 📧 SMS

---

## ❓ Troubleshooting

### "No API key"
- Get free key: https://aistudio.google.com/app/apikey

### "WhatsApp not working"
- Make sure you added credentials in Settings
- Twilio needs verified number

### "Can't access from phone"
- Make sure both devices on same WiFi
- Use your computer's IP address, not localhost

---

## 📞 Support

If you need help:
1. Check GitHub issues
2. Check the SETUP.md in the repo
3. Ask in the community!

---

**Version:** 3.2  
**Date:** April 2026  
**Goal:** Download, run, works!