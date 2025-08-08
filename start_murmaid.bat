@echo off
:: start_murmaid.bat

chcp 65001 >nul
setlocal EnableDelayedExpansion

# turn off pip's own version nags
set PIP_DISABLE_PIP_VERSION_CHECK=1

set VENV_DIR=.venv
set TMP_PIP_REQ=%TEMP%\murmaid_pip_req.txt
set TMP_PIP_UPG=%TEMP%\murmaid_pip_upg.txt

echo ============================================
echo 🧜‍♀️  Murmaid – Local AI voice assistant
echo ============================================

# pull latest
echo 🔄 Checking for updates from GitHub...
git pull

# check python
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo ➡️ Please install Python 3.10 or newer from: https://www.python.org/downloads/
    pause
    exit /b
)

# venv
if not exist %VENV_DIR% (
    echo 🐍 Creating virtual environment...
    python -m venv %VENV_DIR%
)

# activate venv
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b
)
echo ✅ Virtual environment activated

# remember current pip version
for /f "tokens=2 delims= " %%A in ('python -m pip --version') do set OLD_PIP_VER=%%A

# try upgrade pip quietly; capture any output
python -m pip install --upgrade pip -q >"%TMP_PIP_UPG%" 2>&1

# read new pip version
for /f "tokens=2 delims= " %%A in ('python -m pip --version') do set NEW_PIP_VER=%%A

# report only if version actually changed
if not "%OLD_PIP_VER%"=="%NEW_PIP_VER%" (
    echo ⬆️  Upgraded pip: %OLD_PIP_VER% → %NEW_PIP_VER%
)

# install deps quietly; print only if something changed
echo 📦 Installing dependencies...
pip install -q -r requirements.txt >"%TMP_PIP_REQ%" 2>&1

for %%I in ("%TMP_PIP_REQ%") do set SIZE=%%~zI
if "%SIZE%"=="0" (
    echo ✅ Dependencies already up to date.
) else (
    echo 📦 Installed/updated packages:
    type "%TMP_PIP_REQ%"
)

# ssh config for huggingface (only if missing)
set "SSH_CONFIG_PATH=%USERPROFILE%\.ssh\config"
findstr /C:"Host huggingface.co" "%SSH_CONFIG_PATH%" >nul 2>nul
if errorlevel 1 (
    echo 🔐 SSH config for Hugging Face not found – running setup...
    python setup_ssh.py
) else (
    echo ✅ SSH for Hugging Face already configured.
)

# dia tts setup (will be quiet unless it outputs something meaningful)
echo 🔧 Setting up Dia (text-to-speech)...
python setup_dia.py

# cleanup temp files
if exist "%TMP_PIP_REQ%" del "%TMP_PIP_REQ%" >nul 2>&1
if exist "%TMP_PIP_UPG%" del "%TMP_PIP_UPG%" >nul 2>&1

# launch app
echo 🚀 Launching Murmaid on http://127.0.0.1:8000
uvicorn app:app --reload

endlocal
pause
