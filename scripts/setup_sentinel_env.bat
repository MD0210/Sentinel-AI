@echo off
REM Sentinel AI - Download wheels, recreate venv, and install offline.
setlocal

cd /d "%~dp0.."

echo.
echo ==========================================
echo       Sentinel AI Environment Setup
echo ==========================================
echo.

REM ------------------------------------------
REM Step 1: Check requirements file
REM ------------------------------------------

if not exist "requirements-voice.txt" (
    echo ERROR: requirements-voice.txt was not found.
    pause
    exit /b 1
)

REM ------------------------------------------
REM Step 2: Create wheel directory
REM ------------------------------------------

if not exist "wheel" (
    echo Creating wheel directory...
    mkdir "wheel"
)

echo.
echo [1/4] Downloading required wheel files...
echo.

python -m pip download ^
    --only-binary=:all: ^
    -r "requirements-voice.txt" ^
    -d "wheel"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to download one or more wheel files.
    echo.
    pause
    exit /b 1
)

echo.
echo Wheel files downloaded successfully.

REM ------------------------------------------
REM Step 3: Remove existing virtual environment
REM ------------------------------------------

echo.
echo [2/4] Removing existing virtual environment...

if exist ".venv" (
    echo Removing .venv...
    rmdir /s /q ".venv"

    if errorlevel 1 (
        echo.
        echo ERROR: Could not remove .venv.
        echo Make sure the virtual environment is not currently active.
        echo.
        pause
        exit /b 1
    )
)

echo Existing .venv removed.

REM ------------------------------------------
REM Step 4: Create fresh virtual environment
REM ------------------------------------------

echo.
echo [3/4] Creating new virtual environment...

python -m venv ".venv"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create virtual environment.
    echo.
    pause
    exit /b 1
)

echo New .venv created successfully.

REM ------------------------------------------
REM Step 5: Install packages from wheelhouse
REM ------------------------------------------

echo.
echo [4/4] Installing packages from local wheel files...
echo.
echo No PyPI access will be used.
echo.

".venv\Scripts\python.exe" -m pip install ^
    --no-index ^
    --find-links "wheel" ^
    -r "requirements-voice.txt"

if errorlevel 1 (
    echo.
    echo ==========================================
    echo ERROR: Package installation failed.
    echo ==========================================
    echo.
    echo Check that all required wheel files exist
    echo in the wheel folder.
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo       Sentinel AI Setup Complete
echo ==========================================
echo.
echo Virtual environment:
echo     .venv
echo.
echo Packages were installed from:
echo     wheel\
echo.
echo To activate the environment manually:
echo     .venv\Scripts\Activate.ps1
echo.
echo You can now run Sentinel AI.
echo.

pause
exit /b 0