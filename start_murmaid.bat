@echo off
:: start_murmaid.bat

chcp 65001 >nul
setlocal EnableDelayedExpansion

:: env / paths
set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"

:: make pip quieter and stay in venv
set PIP_DISABLE_PIP_VERSION_CHECK=1
set PIP_REQUIRE_VIRTUALENV=1

echo ============================================
echo 🧜‍♀️  Murmaid – Local AI voice assistant
echo ============================================

:: Pull latest changes from GitHub
echo 🔄 Checking for updates from GitHub...
git pull

:: Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo ➡️ Please install Python 3.10 or newer from: https://www.python.org/downloads/
    pause
    exit /b
)

:: Create virtual environment if needed
if not exist "%VENV_DIR%" (
    echo 🐍 Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

:: Activate environment
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b
)
echo ✅ Virtual environment activated

:: Ensure variables point to venv python/pip
if not exist "%VENV_PY%" (
    echo ❌ Missing venv python at "%VENV_PY%".
    pause
    exit /b
)

:: Upgrade pip quietly; only announce if version changed
for /f "tokens=2 delims= " %%A in ('"%VENV_PY%" -m pip --version') do set OLD_PIP_VER=%%A
"%VENV_PY%" -m pip install --upgrade pip -q >"%TEMP%\mur_pip_up.txt" 2>&1
for /f "tokens=2 delims= " %%A in ('"%VENV_PY%" -m pip --version') do set NEW_PIP_VER=%%A
if not "%OLD_PIP_VER%"=="%NEW_PIP_VER%" echo ⬆️  Upgraded pip: %OLD_PIP_VER% → %NEW_PIP_VER%

:: Install deps quietly; print only if something happened
echo 📦 Installing dependencies...
"%VENV_PY%" -m pip install -q -r requirements.txt >"%TEMP%\mur_pip_req.txt" 2>&1
for %%I in ("%TEMP%\mur_pip_req.txt") do set SIZE=%%~zI
if "%SIZE%"=="0" (
    echo ✅ Dependencies already up to date.
) else (
    echo 📦 Installed/updated packages:
    type "%TEMP%\mur_pip_req.txt"
)

:: Conditionally configure SSH for Hugging Face
set "SSH_CONFIG_PATH=%USERPROFILE%\.ssh\config"
findstr /C:"Host huggingface.co" "%SSH_CONFIG_PATH%" >nul 2>nul
if errorlevel 1 (
    echo 🔐 SSH config for Hugging Face not found – running setup...
    "%VENV_PY%" setup_ssh.py
) else (
    echo ✅ SSH for Hugging Face already configured.
)

:: Download and set up Dia (text-to-speech) with venv python
echo 🔧 Setting up Dia (text-to-speech)...
"%VENV_PY%" setup_dia.py

:: Cleanup
if exist "%TEMP%\mur_pip_up.txt" del "%TEMP%\mur_pip_up.txt" >nul 2>&1
if exist "%TEMP%\mur_pip_req.txt" del "%TEMP%\mur_pip_req.txt" >nul 2>&1

:: Start the FastAPI app
echo 🚀 Launching Murmaid on http://127.0.0.1:8000
uvicorn app:app --reload

endlocal
pause
