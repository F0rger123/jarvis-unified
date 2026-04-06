@echo off
setlocal EnableDelayedExpansion

:: ═══════════════════════════════════════════════════════════════════
::  JARVIS v4.0.2 - IMPROVED ONE-CLICK INSTALLER
::  With REAL error messages + GUI progress
:: ═══════════════════════════════════════════════════════════════════

title Jarvis v4.0.2 Installer
color 0a
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║           🤖 JARVIS v4.0.2 - INSTALLER              ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

set ERROR_LOG=%TEMP%\jarvis_error_%date:~4,4%%date:~7,2%%date:~10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set ERROR_LOG=%ERROR_LOG: =0%

:: ═══════════════════════════════════════════════════════════
:: STEP 1: Check Python
:: ═══════════════════════════════════════════════════════════
echo [1/6] Checking Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.10+ from https://python.org
    echo.
    echo After installing, run this installer again.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo       Found: %PYTHON_VER%

:: ═══════════════════════════════════════════════════════════
:: STEP 2: Create virtual environment
:: ═══════════════════════════════════════════════════════════
echo [2/6] Creating virtual environment...

if exist "venv" (
    echo       Using existing venv...
) else (
    python -m venv "venv" 2>> %ERROR_LOG%
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv!
        type %ERROR_LOG%
        pause
        exit /b 1
    )
    echo       Created venv
)

:: ═══════════════════════════════════════════════════════════
:: STEP 3: Install dependencies
:: ═══════════════════════════════════════════════════════════
echo [3/6] Installing dependencies...

call venv\Scripts\activate.bat

pip install -q flask flask-cors requests pyttsx3 2>> %ERROR_LOG%
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    type %ERROR_LOG%
    pause
    exit /b 1
)

echo       Dependencies installed

:: ═══════════════════════════════════════════════════════════════════
:: STEP 4: Test imports
:: ════════════════════════════════════════════════��══════════
echo [4/6] Testing Jarvis imports...

python test_jarvis.py 2>> %ERROR_LOG%
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Jarvis import test FAILED!
    echo.
    echo See errors above. Common fixes:
    echo 1. Make sure you're in the right folder
    echo 2. Delete venv folder and try again
    echo.
    type %ERROR_LOG%
    pause
    exit /b 1
)

echo       Import test passed!

:: ═══════════════════════════════════════════════════════════
:: STEP 5: Create config
:: ═══════════════════════════════════════════════════════════
echo [5/6] Configuring Jarvis...

if not exist "jarvis\.env" (
    (
        echo # Jarvis v4.0.2 Configuration
        echo AI_PROVIDER=gemini
        echo GEMINI_MODEL=gemini-3.1-flash-lite
        echo USE_GEMMA_FOR_CODE=true
        echo CONFIRM_PAYMENTS=true
        echo CONFIRM_ORDERS=true
        echo CONFIRM_SMS=true
        echo CONFIRM_WHATSAPP=true
        echo UI_THEME=tron
        echo ACCENT_COLOR=#00ffff
        echo JARVIS_TONE=helpful
        echo PORT=5000
        echo.
        echo # Add your API key below
        echo GEMINI_API_KEY=
    ) > jarvis\.env
)

:: ═══════════════════════════════════════════════════════════
:: STEP 6: Start server
:: ═══════════════════════════════════════════════════════════
echo [6/6] Starting Jarvis server...
echo.

:: Start server and capture output
echo Starting server on http://localhost:5000 ...
echo.

cd jarvis
start /b cmd /c "call ..\venv\Scripts\activate.bat && python main.py --web >> ..\server.log 2>&1"
cd ..

:: Wait and check if server responds
echo Waiting for server to start...
set SERVER_READY=0
for /L %%i in (1,1,10) do (
    timeout /t 1 /nobreak >nul
    curl -s http://localhost:5000 >nul 2>&1
    if !errorlevel! equ 0 (
        set SERVER_READY=1
        echo Server responded after %%i seconds!
        goto :SERVER_STARTED
    )
    echo   Trying... %%i/10
)

:SERVER_STARTED
if %SERVER_READY% equ 0 (
    echo.
    echo [WARNING] Server may not be ready yet.
    echo Checking server log...
    if exist server.log (
        type server.log
    )
)

:: Wait a bit more
timeout /t 3 /nobreak >nul

:: Final check
curl -s http://localhost:5000 >nul 2>&1
if %errorlevel% equ 0 (
    goto :OPEN_BROWSER
) else (
    echo.
    echo [ERROR] Server is not responding!
    echo.
    echo Server log:
    if exist server.log (
        type server.log
    ) else (
        echo (no server.log found)
    )
    echo.
    echo Try running: python jarvis\main.py --web
    echo to see the error in full.
    pause
    exit /b 1
)

:OPEN_BROWSER
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              ✅ JARVIS v4.0.2 IS READY!                     ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 🌐 Opening http://localhost:5000 ...
echo.

start http://localhost:5000
timeout /t 2 /nobreak >nul

echo.
echo If browser didn't open, go to: http://localhost:5000
echo.
echo NOTE: Add your API key in Settings if not already added!
echo Get free key from: https://aistudio.google.com/app/apikey
echo.
echo Press any key to open settings...
pause >nul

start http://localhost:5000/#settings

exit