# Local Setup Guide

Quick instructions for setting up Sentinel AI on a new Windows machine.

## Requirements

- Windows
- Python 3.12
- Git

## Setup

Clone the repository:

```powershell
git clone https://github.com/MD0210/Sentinel-AI.git
cd Sentinel-AI
```

Run the environment setup:

```powershell
scripts\\setup_sentinel_env.bat
```

Activate the virtual environment:

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

Run the tests:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Voice Enrollment

Create a local voice profile:

```powershell
python scripts/enroll_voice.py
```

Follow the prompts and speak naturally.

Raw recordings are kept in memory only. The generated `config/voice_profile.json` is local and ignored by Git.

## Run Sentinel

```powershell
python main.py
```

## Notes

- Do not commit `.env`, voice profiles, model files, or wheel files.
- For development details and architecture, see the main [README](README.md).
