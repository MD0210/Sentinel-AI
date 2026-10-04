@echo off
REM Sentinel AI - Complete environment setup
REM Checks Python, checks/downloads required wheels,
REM recreates .venv, installs from local wheels, and verifies installation.

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

echo [1/6] Checking for Python...
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

REM Check Python again
where python >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python is installed but is not available in PATH.
    echo.
    echo Please close this window, open a new Command Prompt,
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
echo [2/6] Checking requirements...
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
REM STEP 3 - CHECK WHEELHOUSE
REM ============================================================

echo.
echo [3/6] Checking local wheelhouse...
echo.

if not exist "wheel" (
    echo Creating wheel directory...
    mkdir "wheel"

    if errorlevel 1 (
        echo ERROR: Could not create wheel directory.
        pause
        exit /b 1
    )
)

echo.
echo Checking whether required packages have local wheels...
echo.

REM ------------------------------------------------------------
REM We use pip download to resolve the requirements.
REM Existing wheels are reused when compatible wheels already
REM exist in the wheel directory.
REM ------------------------------------------------------------

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
echo [4/6] Recreating virtual environment...
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
echo [5/6] Installing packages from wheelhouse...
echo.

echo Installation source:
echo     %CD%\wheel
echo.

echo PyPI access is disabled for this installation.
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
REM STEP 6 - VERIFY ENVIRONMENT
REM ============================================================

echo.
echo [6/6] Verifying installation...
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
echo To activate the environment:
echo     .venv\Scripts\Activate.ps1
echo.
echo ==========================================
echo.

pause
exit /b 0