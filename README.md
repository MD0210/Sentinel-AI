# Sentinel AI

A local, voice-authenticated AI assistant for Windows.

## Quick Start

### 1. Install Python

Install **Python 3.12** on Windows.

### 2. Clone the repository

```powershell
git clone https://github.com/MD0210/Sentinel-AI.git
cd Sentinel-AI
```

### 3. Run the setup

From PowerShell:

```powershell
scripts\\setup_sentinel_env.bat
```

This creates a local `.venv` and installs the required dependencies.

If PowerShell blocks script execution, you can use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 4. Activate the environment

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

### 5. Run the tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

All tests should pass before continuing.

## Voice Enrollment

Create your local voice profile:

```powershell
python scripts/enroll_voice.py
```

Follow the prompts and speak naturally.

**Important:** raw recordings are kept in memory only. The local voice profile is stored in:

```text
config/voice_profile.json
```

This file is ignored by Git and should never be committed.

## Run Sentinel

```powershell
python main.py
```

The current development flow is:

```text
Wake phrase → Voice verification → Q&A fallback → Authenticated session
```

## Security

- Never commit `.env`, voice profiles, model files, or wheel files.
- Voice data stays local.
- Authentication failures are rate-limited and locked out.
- Sensitive challenge answers are stored as salted hashes.
- Consequential or destructive actions should require confirmation.

## Development

Use a feature branch for changes:

```powershell
git checkout -b feature/my-change
```

Run the tests before opening a pull request.

## Current Status

Sentinel AI is an early-stage project. Microphone input, voice enrollment, speaker verification, security fallback, and the local development environment are implemented. Additional AI, GitHub, VS Code, filesystem, terminal, and Azure capabilities are being added incrementally.
