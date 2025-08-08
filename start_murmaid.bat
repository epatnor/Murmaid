@echo off
:: start_murmaid.bat

chcp 65001 >nul
setlocal EnableDelayedExpansion

set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "DRYRUN_LOG=%TEMP%\murmaid_pip_dryrun.txt"

set PIP_DISABLE_PIP_VERSION_CHECK=1
set PIP_REQUIRE_VIRTUALENV=1

echo ============================================
echo 🧜‍♀️  Murmaid – Local AI voice assistant
echo ============================================

echo 🔄 Checking for updates from GitHub...
git pull

where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    pause
    exit /b
)

if not exist "%VENV_DIR%" (
    echo 🐍 Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b
)
echo ✅ Virtual environment activated

:: upgrade pip quietly
for /f "tokens=2 delims= " %%A in ('"%VENV_PY%" -m pip --version') do set OLD_PIP_VER=%%A
"%VENV_PY%" -m pip install --upgrade pip -q >nul 2>&1
for /f "tokens=2 delims= " %%A in ('"%VENV_PY%" -m pip --version') do set NEW_PIP_VER=%%A
if not "%OLD_PIP_VER%"=="%NEW_PIP_VER%" echo ⬆️  Upgraded pip: %OLD_PIP_VER% → %NEW_PIP_VER%

:: dry-run to detect changes
echo 📦 Installing dependencies...
"%VENV_PY%" -m pip install --dry-run -r requirements.txt >"%DRYRUN_LOG%" 2>&1

for %%I in ("%DRYRUN_LOG%") do set SIZE=%%~zI
if "%SIZE%"=="0" (
    echo ✅ Dependencies already up to date.
) else (
    echo 🔧 Changes detected – installing...
    type "%DRYRUN_LOG%"
    "%VENV_PY%" -m pip install -r requirements.txt
)

:: SSH config
set "SSH_CONFIG_PATH=%USERPROFILE%\.ssh\config"
findstr /C:"Host huggingface.co" "%SSH_CONFIG_PATH%" >nul 2>nul
if errorlevel 1 (
    echo 🔐 SSH config for Hugging Face not found – running setup...
    "%VENV_PY%" setup_ssh.py
) else (
    echo ✅ SSH for Hugging Face already configured.
)

:: Dia setup
echo 🔧 Setting up Dia (text-to-speech)...
"%VENV_PY%" setup_dia.py

:: cleanup
if exist "%DRYRUN_LOG%" del "%DRYRUN_LOG%" >nul 2>&1

echo 🚀 Launching Murmaid on http://127.0.0.1:8000
uvicorn app:app --reload

endlocal
pause
