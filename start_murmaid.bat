@echo off
:: start_murmaid.bat

chcp 65001 >nul
setlocal EnableDelayedExpansion

:: paths
set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"
set "DRYRUN_JSON=%TEMP%\murmaid_pip_dryrun.json"

:: pip behavior
set PIP_DISABLE_PIP_VERSION_CHECK=1
set PIP_REQUIRE_VIRTUALENV=1

echo ============================================
echo 🧜‍♀️  Murmaid – Local AI voice assistant
echo ============================================

echo 🔄 Checking for updates from GitHub...
git pull

:: ensure python exists
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo ➡️ Install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b
)

:: ensure venv
if not exist "%VENV_DIR%" (
    echo 🐍 Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

:: activate venv
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment.
    pause
    exit /b
)
echo ✅ Virtual environment activated

:: upgrade pip quietly, only announce if changed
for /f "tokens=2 delims= " %%A in ('"%VENV_PY%" -m pip --version') do set OLD_PIP_VER=%%A
"%VENV_PY%" -m pip install --upgrade pip -q >nul 2>&1
for /f "tokens=2 delims= " %%A in ('"%VENV_PY%" -m pip --version') do set NEW_PIP_VER=%%A
if not "%OLD_PIP_VER%"=="%NEW_PIP_VER%" echo ⬆️  Upgraded pip: %OLD_PIP_VER% → %NEW_PIP_VER%

:: dry-run to detect if anything would be installed/updated
echo 📦 Installing dependencies...
if exist "%DRYRUN_JSON%" del "%DRYRUN_JSON%" >nul 2>&1
"%VENV_PY%" -m pip install --dry-run -q --no-input --report "%DRYRUN_JSON%" -r requirements.txt 2>nul

:: Does the report include planned installs/updates?
:: We'll let PowerShell count the number of "install" actions in the JSON; 0 means up to date.
for /f "usebackq tokens=* delims=" %%C in (`powershell -NoProfile -Command ^
  "if (Test-Path '%DRYRUN_JSON%') {try{($json=Get-Content -Raw '%DRYRUN_JSON%'|ConvertFrom-Json); ($json.install|Measure-Object).Count}catch{0}} else {0}"`) do set INSTALL_COUNT=%%C

if "%INSTALL_COUNT%"=="0" (
    echo ✅ Dependencies already up to date.
) else (
    echo 🔧 Changes detected: %INSTALL_COUNT% package(s) will be installed/updated.
    echo ⏳ Running pip install (showing progress)...
    "%VENV_PY%" -m pip install --no-input -r requirements.txt
)

:: SSH for Hugging Face
set "SSH_CONFIG_PATH=%USERPROFILE%\.ssh\config"
findstr /C:"Host huggingface.co" "%SSH_CONFIG_PATH%" >nul 2>nul
if errorlevel 1 (
    echo 🔐 SSH config for Hugging Face not found – running setup...
    "%VENV_PY%" setup_ssh.py
) else (
    echo ✅ SSH for Hugging Face already configured.
)

:: Dia setup (runs under venv python)
echo 🔧 Setting up Dia (text-to-speech)...
"%VENV_PY%" setup_dia.py

:: cleanup
if exist "%DRYRUN_JSON%" del "%DRYRUN_JSON%" >nul 2>&1

echo 🚀 Launching Murmaid on http://127.0.0.1:8000
uvicorn app:app --reload

endlocal
pause
