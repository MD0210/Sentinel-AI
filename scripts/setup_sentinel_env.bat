@echo off
REM Sentinel AI - Complete environment setup
REM Checks Python, downloads required wheels, recreates .venv,
REM installs packages, downloads the openWakeWord model,
REM and verifies the environment.

setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0.."

echo.
echo ==========================================
echo       Sentinel AI Environment Setup
echo ==========================================
echo.

REM ============================================================
REM STEP 1 - CHECK PYTHON
REM ============================================================

echo [1/7] Checking for Python...
echo.

where python >nul 2>&1

if errorlevel 1 (
    echo Python was not found.
    echo.
    echo Attempting to install Python 3.12 using winget...
    echo.

    where winget >nul 2>&1

    if errorlevel 1 (
        echo ERROR: winget is not available.
        echo Please install Python 3.12 manually.
        echo.
        pause
        exit /b 1
    )

    winget install ^
        --id Python.Python.3.12 ^
        --exact ^
        --scope user ^
        --accept-source-agreements ^
        --accept-package-agreements

    if errorlevel 1 (
        echo.
        echo ERROR: Python installation failed.
        echo.
        pause
        exit /b 1
    )

    echo.
    echo Python installation completed.
    echo.
)

where python >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python is installed but is not available in PATH.
    echo.
    echo Close this window, open a new Command Prompt,
    echo and run this script again.
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version

if errorlevel 1 (
    echo.
    echo ERROR: Python could not be executed.
    echo.
    pause
    exit /b 1
)

REM ============================================================
REM STEP 2 - CHECK REQUIREMENTS
REM ============================================================

echo.
echo [2/7] Checking requirements...
echo.

if not exist "requirements-voice.txt" (
    echo ERROR: requirements-voice.txt was not found.
    echo.
    echo Expected:
    echo     %CD%\requirements-voice.txt
    echo.
    pause
    exit /b 1
)

echo Found:
echo     requirements-voice.txt

REM ============================================================
REM STEP 3 - CHECK / DOWNLOAD WHEELS
REM ============================================================

echo.
echo [3/7] Checking local wheelhouse...
echo.

if not exist "wheel" (
    echo Creating wheel directory...
    mkdir "wheel"

    if errorlevel 1 (
        echo ERROR: Could not create wheel directory.
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Downloading required Python wheels...
echo.

python -m pip download ^
    --only-binary=:all: ^
    -r "requirements-voice.txt" ^
    -d "wheel"

if errorlevel 1 (
    echo.
    echo ERROR: Could not obtain all required wheel files.
    echo.
    echo Possible causes:
    echo   - No compatible wheel exists for this Python version.
    echo   - Internet connection is unavailable.
    echo   - A package requires a source build.
    echo.
    pause
    exit /b 1
)

echo.
echo Wheelhouse is ready.

echo.
echo Available wheel files:
echo ------------------------------------------

dir /b "wheel\*.whl"

echo ------------------------------------------

REM ============================================================
REM STEP 4 - REMOVE AND RECREATE VENV
REM ============================================================

echo.
echo [4/7] Recreating virtual environment...
echo.

if exist ".venv" (
    echo Removing existing .venv...
    echo.

    rmdir /s /q ".venv"

    if errorlevel 1 (
        echo.
        echo ERROR: Could not remove .venv.
        echo.
        echo Make sure the existing virtual environment
        echo is not currently active.
        echo.
        pause
        exit /b 1
    )

    echo Existing .venv removed.
)

echo.
echo Creating new virtual environment...

python -m venv ".venv"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create .venv.
    echo.
    pause
    exit /b 1
)

echo.
echo New virtual environment created successfully.

REM ============================================================
REM STEP 5 - INSTALL FROM LOCAL WHEELS ONLY
REM ============================================================

echo.
echo [5/7] Installing packages from wheelhouse...
echo.

echo Installation source:
echo     %CD%\wheel
echo.

echo PyPI access is disabled for package installation.
echo.

".venv\Scripts\python.exe" -m pip install ^
    --no-index ^
    --find-links "%CD%\wheel" ^
    -r "requirements-voice.txt"

if errorlevel 1 (
    echo.
    echo ==========================================
    echo ERROR: Offline installation failed.
    echo ==========================================
    echo.
    echo Check the wheel directory:
    echo     %CD%\wheel
    echo.
    echo The required wheels may not be compatible
    echo with the installed Python version.
    echo.
    pause
    exit /b 1
)

REM ============================================================
REM STEP 6 - DOWNLOAD OPENWAKEWORD MODEL
REM ============================================================

echo.
echo [6/7] Downloading openWakeWord model...
echo.

echo Required acoustic model:
echo     hey_jarvis_v0.1
echo.

echo Downloading model files...
echo.

".venv\Scripts\python.exe" -c "import openwakeword.utils as u; u.download_models(['hey_jarvis_v0.1'])"

if errorlevel 1 (
    echo.
    echo ==========================================
    echo ERROR: Wake-word model download failed.
    echo ==========================================
    echo.
    echo Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo Wake-word model download command completed.

REM ============================================================
REM VERIFY MODEL FILE
REM ============================================================

echo.
echo Verifying wake-word model file...
echo.

".venv\Scripts\python.exe" -c "from pathlib import Path; import openwakeword; p=Path(openwakeword.__file__).parent/'resources'/'models'/'hey_jarvis_v0.1.onnx'; print('Model:', p); print('Exists:', p.exists()); raise SystemExit(0 if p.exists() else 1)"

if errorlevel 1 (
    echo.
    echo ==========================================
    echo ERROR: Wake-word model file was not found.
    echo ==========================================
    echo.
    echo Expected:
    echo     .venv\Lib\site-packages\openwakeword\resources\models\hey_jarvis_v0.1.onnx
    echo.
    echo The download did not place the model where
    echo openWakeWord expects it.
    echo.
    pause
    exit /b 1
)

echo.
echo Wake-word model verified successfully.

REM ============================================================
REM STEP 7 - VERIFY ENVIRONMENT
REM ============================================================

echo.
echo [7/7] Verifying installation...
echo.

echo Python version:
".venv\Scripts\python.exe" --version

if errorlevel 1 (
    echo.
    echo ERROR: Python verification failed.
    echo.
    pause
    exit /b 1
)

echo.
echo Installed packages:
echo ------------------------------------------

".venv\Scripts\python.exe" -m pip list

if errorlevel 1 (
    echo.
    echo ERROR: Could not verify installed packages.
    echo.
    pause
    exit /b 1
)

echo ------------------------------------------

echo.
echo ==========================================
echo       Sentinel AI Setup Complete
echo ==========================================
echo.
echo Virtual environment:
echo     .venv\
echo.
echo Wheelhouse:
echo     wheel\
echo.
echo Requirements:
echo     requirements-voice.txt
echo.
echo Wake-word model:
echo     hey_jarvis_v0.1
echo.
echo To activate the environment:
echo     .venv\Scripts\Activate.ps1
echo.
echo ==========================================
echo.

pause
exit /b 0