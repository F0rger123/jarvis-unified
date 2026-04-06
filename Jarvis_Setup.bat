@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: JARVIS v5.0 - ONE-CLICK SETUP
:: ============================================================
cd /d "%~dp0"
title Jarvis Setup

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║              🤖 JARVIS v5.0 - SETUP                      ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: ============================================================
:: [1/6] CHECK PYTHON
:: ============================================================
echo [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ from https://python.org
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo       Found: %PYTHON_VER%

:: ============================================================
:: [2/6] CREATE VIRTUAL ENVIRONMENT
:: ============================================================
echo [2/6] Creating virtual environment...

if exist "venv" (
    echo       Using existing venv...
) else (
    python -m venv "venv" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to create venv!
        pause
        exit /b 1
    )
    echo       Created venv
)

:: ============================================================
:: [3/6] INSTALL DEPENDENCIES
:: ============================================================
echo [3/6] Installing dependencies...

call "venv\Scripts\activate.bat"
pip install -q flask flask-cors google-generativeai python-dotenv requests 2>nul
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo       Dependencies installed

:: ============================================================
:: [4/6] CONFIGURE
:: ============================================================
echo [4/6] Configuring Jarvis...

if not exist "jarvis\.env" (
    mkdir jarvis >nul 2>&1
    (
        echo AI_PROVIDER=gemini
        echo GEMINI_MODEL=gemini-3.1-flash-lite
        echo USE_GEMMA_FOR_CODE=true
        echo CONFIRM_PAYMENTS=true
        echo CONFIRM_ORDERS=true
        echo CONFIRM_SMS=true
        echo CONFIRM_WHATSAPP=true
        echo UI_THEME=tron
        echo ACCENT_COLOR=#00ffff
        echo.
        echo GEMINI_API_KEY=
    ) > "jarvis\.env"
)
echo       Config created

:: ============================================================
:: [5/6] API KEY
:: ============================================================
echo [5/6] API Key setup...

call :get_api_key
goto :skip_get_api_key

:get_api_key
set api_key=
echo.
echo ⚠️  IMPORTANT: Add your API key to use Jarvis!
echo.
echo 1. Get free key from: https://aistudio.google.com/app/apikey
echo 2. Copy the key (starts with AI...)
echo.
set /p api_key="Paste API key here: "
if not defined api_key (
    echo.
    echo Skipping - you can add key later in jarvis\.env
    goto :api_done
)
echo GEMINI_API_KEY=%api_key%>> "jarvis\.env"
echo ✅ API key saved!
:api_done
exit /b

:skip_get_api_key

:: ============================================================
:: [6/6] START JARVIS
:: ============================================================
echo [6/6] Starting Jarvis...
echo.

cd jarvis
start /b cmd /c "call ..\venv\Scripts\activate.bat && python main.py --web"
cd ..

:: Wait for server
echo Waiting for server...
ping -n 5 127.0.0.1 >nul 2>&1

:: Check if server is running
curl -s http://localhost:5000 >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Server may take a moment to start...
    ping -n 3 127.0.0.1 >nul 2>&1
)

:: ============================================================
:: DONE
:: ============================================================
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║              ✅ JARVIS IS READY!                        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo 🌐 Opening browser...
echo.

start http://localhost:5000

echo If browser didn't open, go to: http://localhost:5000
echo.
echo Press any key to exit...
pause >nul
exit