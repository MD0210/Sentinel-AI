# Sentinel AI — Beginner Setup Guide

This guide is written for someone who is **new to programming** and wants to set up Sentinel AI on a Windows computer.

You do not need to understand the code before starting. Follow the steps in order and copy the commands exactly.

> **Important:** Sentinel AI is a local development project. Some steps install Python packages and download a local AI voice model. This can take some time and may use several gigabytes of disk space.

## 1. What you need before starting

You need:
- A Windows PC
- An internet connection
- A microphone
- A GitHub account
- **Git** installed
- **Python 3.12** installed
- **Visual Studio Code (VS Code)** installed (recommended)

### What are these programs?

- **Python** — the programming language Sentinel AI uses.
- **Git** — downloads the Sentinel AI project from GitHub and tracks changes.
- **VS Code** — the application where you view and edit project files.
- **PowerShell** — a Windows terminal where you type commands.

## 2. Open VS Code or PowerShell

### Recommended: VS Code

1. Click the **Windows Start** button.
2. Search for **Visual Studio Code**.
3. Open **Visual Studio Code**.
4. Click **Terminal** in the top menu.
5. Click **New Terminal**.
6. A terminal panel appears at the bottom.
7. Make sure the terminal is **PowerShell**.

This lets you edit the project and run commands in the same window.

### Alternative: Windows PowerShell

1. Click **Start**.
2. Search for **PowerShell**.
3. Open **Windows PowerShell**.

The commands in this guide work in either PowerShell window.

## 3. Download Sentinel AI from GitHub

In PowerShell, run:

```powershell
cd "$HOME\Documents"
git clone https://github.com/MD0210/Sentinel-AI.git
cd Sentinel-AI
```

What these commands mean:
- `cd` = change folder.
- `git clone` = download the project from GitHub.
- `cd Sentinel-AI` = enter the project folder.

If you use VS Code, open the project with:

```powershell
code .
```

If `code` is not recognized, use **File → Open Folder** in VS Code and select the `Sentinel-AI` folder.

## 4. Make sure you are in the right folder

Run:

```powershell
Get-Location
Get-ChildItem
```

You should see a path ending in something like `Documents\Sentinel-AI` and files/folders such as `README.md`, `SETUP.md`, `main.py`, `agent`, `security`, `voice`, and `tests`.

## 5. Create the Sentinel AI environment

Sentinel AI uses a **virtual environment**. This keeps its Python packages separate from other projects.

From the `Sentinel-AI` folder, run:

```powershell
scripts\setup_sentinel_env.bat
```

Wait for it to finish. Do not close the terminal while setup is running.

### If PowerShell blocks activation

If you see an execution-policy error, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

This only changes the policy for the current PowerShell window.

## 6. Activate the virtual environment

If it is not already active, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

A successful activation normally shows `(.venv)` at the beginning of the prompt, for example:

```text
(.venv) PS C:\Users\YourName\Documents\Sentinel-AI>
```

## 7. Check Python

Run:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

Python should be version 3.12.x, and the executable path should contain `Sentinel-AI\.venv\`.

## 8. Run the tests

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

A successful test run should end with something similar to:

```text
OK
```

If tests fail, do not ignore the error. Keep the error message so it can be investigated.

## 9. Set up your voice profile

Make sure your microphone works and you are somewhere reasonably quiet.

Start enrollment:

```powershell
python scripts/enroll_voice.py
```

Follow the prompts and speak naturally. Do not intentionally change your voice.

The process creates:

```text
config\voice_profile.json
```

The raw microphone recordings are kept in memory for processing. The generated voice profile is local and ignored by Git.

> **Privacy:** A voice profile is biometric information. Do not upload it, commit it, or share it publicly.

## 10. Run Sentinel AI

Run:

```powershell
python main.py
```

The current development version has a wake-call and voice-authentication pipeline. The microphone wake-word implementation is still under development, so the current system should not be assumed to acoustically recognize every spoken Sentinel phrase.

## 11. Authentication and private answers

Sentinel can use voice authentication and a secure two-question fallback.

The fallback answers are sensitive. Never put them in source code, README files, GitHub issues, or pull requests.

The local `.env` file is intentionally ignored by Git.

## 12. Stop Sentinel AI

You can normally type:

```text
exit
```

or:

```text
quit
```

You can also press **Ctrl+C** in PowerShell.

## 13. Beginner Git workflow

For development, do not normally edit `main` directly. Create a branch for your change.

```powershell
git checkout main
git pull
git checkout -b my-change
```

After making your change:

```powershell
git status
git add .
git commit -m "Describe the change"
git push -u origin my-change
```

Then create a Pull Request on GitHub.

The preferred Sentinel AI workflow is:

**Branch → Make change → Test → Commit → Push → Pull Request → Review → Merge**

## 14. Important files and folders

| File/folder | Purpose |
|---|---|
| `main.py` | Starts Sentinel AI |
| `agent/` | Agent/controller logic |
| `security/` | Authentication and authorization |
| `voice/` | Wake-call, recording, enrollment, and voice verification |
| `tests/` | Automated tests |
| `scripts/` | Setup and voice scripts |
| `config/` | Local configuration and voice profile |
| `memory/` | Reserved for future local memory |
| `tools/` | Reserved for future tool integrations |
| `README.md` | Project overview and architecture |
| `SETUP.md` | Beginner setup instructions |

## 15. Files that must not be committed

Never commit:
- `.env`
- `config\voice_profile.json`
- downloaded AI model files
- `pretrained_models\`
- `.venv\`
- local `.whl` files

These are intentionally excluded by `.gitignore`.

Before committing, check:

```powershell
git status
```

If you are unsure whether a file is safe to commit, stop and check before pushing it to GitHub.

## 16. Common beginner problems

### "git is not recognized"

Check:

```powershell
git --version
```

If Git is not installed, install it and restart VS Code or PowerShell.

### "python is not recognized"

Check:

```powershell
python --version
```

If Python was just installed, restart VS Code or PowerShell.

### ".venv\Scripts\Activate.ps1 cannot be loaded"

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### "No module named ..."

Make sure `(.venv)` appears in your PowerShell prompt. If needed, activate it again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then rerun:

```powershell
scripts\setup_sentinel_env.bat
```

### Microphone problems

Check that Windows can see the microphone, it is not muted, and other applications are not exclusively using it.

## 17. Simple daily checklist

For a beginner, this is the basic sequence:

```text
Open VS Code
    ↓
Open PowerShell terminal
    ↓
Enter the Sentinel-AI folder
    ↓
Activate .venv
    ↓
Make a change
    ↓
Run tests
    ↓
Check git status
    ↓
Commit and push
    ↓
Create a Pull Request
```

If you are unsure what Git is about to do, run:

```powershell
git status
```

before making Git changes.

## Related documentation

See `README.md` for the project vision, architecture, security principles, and development status.
