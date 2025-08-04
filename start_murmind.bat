@echo off
:: start_murmind.bat

set VENV_DIR=.venv

echo =====================================
echo 🧠 Starting Murmind setup and server
echo =====================================

:: Kolla att Python är installerat
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo ➡️ Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b
)

:: Skapa virtuell miljö om den inte finns
if not exist %VENV_DIR% (
    echo 🐍 Creating virtual environment...
    python -m venv %VENV_DIR%
)

:: Aktivera miljön
call %VENV_DIR%\Scripts\activate

:: Installera beroenden
echo 📦 Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Installera och konfigurera Dia
echo 🔧 Setting up Dia...
python setup_dia.py

:: Starta FastAPI-servern
echo 🚀 Launching Murmind on http://127.0.0.1:8000
uvicorn app:app --reload

pause
