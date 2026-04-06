@echo off
setlocal EnableDelayedExpansion

:: ═══════════════════════════════════════════════════════════════════
::  JARVIS v4.0 - TRUE ONE-CLICK INSTALLER (NO TERMINAL NEEDED!)
:: ═══════════════════════════════════════════════════════════════════

title Jarvis v4.0 Installer
color 0a
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║           🤖 JARVIS v4.0 - ONE CLICK INSTALL             ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% equ 0 goto :PYTHON_FOUND

:: Python not found - try to install silently
echo [1/5] Python not found. Installing silently...

:: Download and install Python silently
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile '%TEMP%\python_installer.exe'" >nul 2>&1
start /wait %TEMP%\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
del %TEMP%\python_installer.exe 2>nul

:: Refresh PATH
set PATH=C:\Program Files\Python312;C:\Program Files\Python312\Scripts;%PATH%

:: Verify install
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python installation failed.
    echo Please download Python manually from https://python.org
    pause
    exit /b 1
)

:PYTHON_FOUND
echo [2/5] Python found - Creating virtual environment...

:: Create venv
python -m venv "%~dp0venv" >nul 2>&1
call "%~dp0venv\Scripts\activate.bat"

echo [3/5] Installing dependencies...
pip install -q flask flask-cors requests pyttsx3 pillow pydub twilio selenium 2>nul

echo [4/5] Configuring Jarvis...

:: Create .env with defaults
echo # Jarvis v4.0 Configuration> "%~dp0jarvis\.env"
echo AI_PROVIDER=gemini>> "%~dp0jarvis\.env"
echo GEMINI_MODEL=gemini-3.1-flash-lite>> "%~dp0jarvis\.env"
echo USE_GEMMA_FOR_CODE=true>> "%~dp0jarvis\.env"
echo CONFIRM_PAYMENTS=true>> "%~dp0jarvis\.env"
echo CONFIRM_ORDERS=true>> "%~dp0jarvis\.env"
echo CONFIRM_SMS=true>> "%~dp0jarvis\.env"
echo CONFIRM_WHATSAPP=true>> "%~dp0jarvis\.env"
echo UI_THEME=tron>> "%~dp0jarvis\.env"
echo ACCENT_COLOR=#00ffff>> "%~dp0jarvis\.env"
echo JARVIS_TONE=helpful>> "%~dp0jarvis\.env"
echo. >> "%~dp0jarvis\.env"
echo # Your API key below>> "%~dp0jarvis\.env"
echo GEMINI_API_KEY=>> "%~dp0jarvis\.env"

:: Copy main.py if not exists
if not exist "%~dp0jarvis\main.py" copy /Y "%~dp0main.py" "%~dp0jarvis\" >nul 2>&1

echo [5/5] Launching Jarvis...

:: Start Jarvis in background
start "" cmd /c "cd /d "%~dp0jarvis" && call venv\Scripts\activate.bat && python main.py --web"

:: Wait a moment
timeout /t 3 /nobreak >nul

:: Open browser
start http://localhost:5000

cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              ✅ JARVIS v4.0 IS READY!                     ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 📌 Jarvis is now open in your browser!
echo.
echo ⚠️  IMPORTANT: Add your API key to continue:
echo.
echo 1. Go to: https://aistudio.google.com/app/apikey
echo 2. Copy your API key
echo 3. Click Settings (gear icon) in Jarvis
echo 4. Paste your API key
echo.
echo Press any key to open settings page...
pause >nul

start http://localhost:5000

exit