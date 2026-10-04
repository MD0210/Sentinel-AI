@echo off
REM Create a clean Sentinel AI virtual environment and install local wheel files.
setlocal
cd /d "%~dp0.."

set "VENV_DIR=.venv"
set "WHEEL_DIR=wheel"

if not exist "%WHEEL_DIR%" (
    echo ERROR: wheel folder was not found.
    exit /b 1
)

if exist "%VENV_DIR%" (
    echo Removing existing .venv...
    rmdir /s /q "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: Could not remove .venv. Make sure it is not in use.
        exit /b 1
    )
)

echo Creating fresh virtual environment...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    exit /b 1
)

echo Installing Sentinel AI voice dependencies from local wheels...
"%VENV_DIR%\Scripts\python.exe" -m pip install --no-index --find-links "%WHEEL_DIR%" -r requirements-voice.txt
if errorlevel 1 (
    echo ERROR: Wheel installation failed. Check that all required wheels are in wheel.
    exit /b 1
)

echo.
echo Sentinel AI virtual environment is ready.
echo Activate it with: .venv\Scripts\Activate.ps1
exit /b 0
