@echo off
:: start_murmaid.bat

chcp 65001 >nul
set VENV_DIR=.venv

echo ============================================
echo 🧜‍♀️  Murmaid – Local AI voice assistant
echo ============================================

:: Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo ➡️ Please install Python 3.10 or newer from: https://www.python.org/downloads/
    pause
    exit /b
)

:: Create virtual environment if needed
if not exist %VENV_DIR% (
    echo 🐍 Creating virtual environment...
    python -m venv %VENV_DIR%
)

:: Activate environment
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b
)
echo ✅ Virtual environment activated

:: Install Python packages
echo 📦 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Conditionally configure SSH for Hugging Face
set SSH_CONFIG_PATH=%USERPROFILE%\.ssh\config

findstr /C:"Host huggingface.co" "%SSH_CONFIG_PATH%" >nul 2>nul
if errorlevel 1 (
    echo 🔐 SSH config for Hugging Face not found – running setup...
    python setup_ssh.py
) else (
    echo ✅ SSH for Hugging Face already configured.
)

:: Download and set up Dia
echo 🔧 Setting up Dia (text-to-speech)...
python setup_dia.py

:: Start the FastAPI app
echo 🚀 Launching Murmaid on http://127.0.0.1:8000
uvicorn app:app --reload

pause
