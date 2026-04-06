@echo off
:: ============================================================
:: JARVIS PORTABLE - Build .EXE from source
:: ============================================================
:: 
:: This script builds a single Jarvis_Portable.exe
:: that runs WITHOUT Python installed!
::
:: Run once on any Windows PC with Python
:: ============================================================

echo.
echo ========================================
echo   JARVIS PORTABLE - BUILD SCRIPT
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    echo Install Python 3.10+ from python.org
    pause
    exit /b 1
)

:: Install PyInstaller
echo [1/3] Installing PyInstaller...
pip install -q pyinstaller

:: Install dependencies
echo [2/3] Installing dependencies...
pip install -q flask flask-cors requests google-generativeai pyttsx3

:: Build exe
echo [3/3] Building Jarvis_Portable.exe...
pyinstaller Jarvis_Portable.spec --clean

echo.
echo ========================================
echo   ✅ BUILD COMPLETE!
echo ========================================
echo.
echo Your .exe is in:
echo   dist\Jarvis_Portable.exe
echo.
echo Copy this .exe to share with anyone!
echo.
pause