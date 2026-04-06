@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   JARVIS v3.3 - Quick Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create venv
    pause
    exit /b 1
)

echo [2/6] Activating environment...
call venv\Scripts\activate.bat

echo [3/6] Installing dependencies...
pip install -q flask flask-cors requests pyttsx3 pillow pydub selenium twilio
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [4/6] Creating .env file...
(
echo # AI Configuration
echo AI_PROVIDER=gemini
echo GEMINI_API_KEY=
echo GEMINI_MODEL=gemini-3.1-flash-lite
echo USE_GEMMA_FOR_CODE=true
echo.
echo # Code Brain
echo GEMMA_4_CODE_BRAIN=gemma-4-9b-it
echo.
echo # Security Confirmations
echo CONFIRM_PAYMENTS=true
echo CONFIRM_ORDERS=true
echo CONFIRM_SMS=true
echo CONFIRM_WHATSAPP=true
echo.
echo # WhatsApp (configure in app Settings)
echo WHATSAPP_ENABLED=false
echo.
echo # UI Theme
echo UI_THEME=tron
echo ACCENT_COLOR=#00ffff
echo.
echo # Voice
echo INPUT_MODE=text
echo.
echo # Server
echo PORT=5000
) > jarvis\.env

echo.
echo ========================================
echo   ⚠️  IMPORTANT: ADD API KEY
echo ========================================
echo.
echo You need a FREE Google Gemini API key:
echo.
echo 1. Go to: https://aistudio.google.com/app/apikey
echo 2. Sign in with your Google account
echo 3. Click "Create API Key"
echo 4. Copy the key
echo.
set /p API_KEY="Paste your API key here: "

if "%API_KEY%"=="" (
    echo No API key entered. You can add it later in jarvis\.env
) else (
    echo GEMINI_API_KEY=%API_KEY% >> jarvis\.env
    echo [SAVED] API key saved to .env
)

echo.
echo [5/6] Testing installation...
python -c "import flask; import requests; print('OK')" 2>nul
if errorlevel 1 (
    echo [WARNING] Some dependencies may not be installed
)

echo [6/6] Launching Jarvis...
echo.
echo ========================================
echo   JARVIS IS READY!
echo ========================================
echo.
echo Open your browser and go to:
echo   http://localhost:5000
echo.
echo If that doesn't work, try:
echo   http://127.0.0.1:5000
echo.
echo To access from PHONE on same WiFi:
echo   http://[YOUR_PC_IP]:5000
echo.
echo (Find your IP with: ipconfig in CMD)
echo.
echo Press any key to start Jarvis...
pause >nul

python jarvis\main.py --web

pause
