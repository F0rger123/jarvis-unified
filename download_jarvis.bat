@echo off
echo ========================================
echo   JARVIS v3.2 - Quick Setup
echo ========================================
echo.

echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo [2/4] Creating virtual environment...
python -m venv venv

echo [3/4] Activating environment...
call venv\Scripts\activate.bat

echo [4/4] Installing dependencies...
pip install -r jarvis\requirements.txt >nul 2>&1

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Get free Gemini API key:
echo    https://aistudio.google.com/app/apikey
echo.
echo 2. Edit jarvis\.env and add your key:
echo    GEMINI_API_KEY=your_key_here
echo.
echo 3. (Optional) Add WhatsApp in Settings UI
echo.
echo 4. Run Jarvis:
echo    python jarvis\main.py --web
echo.
echo 5. Open in browser:
echo    http://localhost:5000
echo.
pause