@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: JARVIS v10.1-DEBUG - Shows REAL errors
:: ============================================================
cd /d "%~dp0"
title Jarvis Setup - DEBUG MODE

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║              🤖 JARVIS v10.1-DEBUG                       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: ============================================================
:: [1/6] CHECK PYTHON
:: ============================================================
echo [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Install Python 3.10+ from https://python.org
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
    python -m venv "venv"
    if errorlevel 1 (
        echo [ERROR] Failed to create venv!
        echo Check error_log.txt
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
call pip install flask flask-cors requests google-generativeai python-dotenv 2>> ..\error_log.txt
if errorlevel 1 (
    echo [ERROR] pip install failed!
    type ..\error_log.txt
    pause
    exit /b 1
)
echo       Dependencies installed

:: ============================================================
:: [4/6] CONFIGURE
:: ============================================================
echo [4/6] Configuring Jarvis...

if not exist "jarvis\.env" (
    mkdir jarvis 2>nul
    (
        echo AI_PROVIDER=gemini
        echo GEMINI_MODEL=gemini-3.1-flash-lite
        echo USE_GEMMA_FOR_CODE=true
        echo.
        echo GEMINI_API_KEY=
    ) > "jarvis\.env"
)

:: Ask for API key if not set
findstr /C:"GEMINI_API_KEY=" "jarvis\.env" | findstr /V /C:"GEMINI_API_KEY=$" >nul
if errorlevel 1 (
    echo.
    echo ⚠️ Enter your API key:
    echo Get free key from: https://aistudio.google.com/app/apikey
    echo.
    set /p API_KEY="Paste API key: "
    if defined API_KEY (
        call powershell -Command "(Get-Content 'jarvis\.env') -replace '^GEMINI_API_KEY=','GEMINI_API_KEY=%API_KEY%' | Set-Content 'jarvis\.env'"
    )
)

:: ============================================================
:: [5/6] START SERVER - SHOW REAL ERRORS
:: ============================================================
echo [5/6] Starting Jarvis server...
echo.
echo Watch for errors below...
echo ========================================
echo.

cd jarvis
:: Run with full error output
python main.py --web 2> ..\error_log.txt
set SERVER_EXIT=%errorlevel%

echo.
echo ========================================
echoServer exited with code: %SERVER_EXIT%
echo.

:: Show error if any
if exist ..\error_log.txt (
    echo ERROR LOG:
    echo ========================================
    type ..\error_log.txt
    echo ========================================
)

:: ============================================================
:: [6/6] RESULTS
:: ============================================================
if %SERVER_EXIT% equ 0 (
    echo Server started OK!
    start http://localhost:5000
) else (
    echo [FAILED] Server did not start!
    echo Check error_log.txt for details
)

echo.
echo Press any key to exit...
pause >nul
exit