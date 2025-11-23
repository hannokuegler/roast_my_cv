# API Key Configuration Guide

This document explains how the project manages API keys securely.

## Overview

The project uses a `config.py` file to store your Gemini API key. This file is:
- NOT tracked by git (listed in .gitignore)
- Automatically loaded by all scripts and notebooks
- Never committed to version control

## Setup Instructions

### Step 1: Get Your API Key

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create a new API key
4. Copy the key

### Step 2: Configure the Project

```bash
# Copy the example template
cp config.example.py config.py

# Edit config.py and replace YOUR_API_KEY_HERE with your actual key
# On Mac/Linux:
nano config.py

# On Windows:
notepad config.py
```

Edit this line:
```python
GEMINI_API_KEY = "---"
```

### Step 3: Verify Setup

Run the setup verification script:
```bash
python check_setup.py
```

You should see:
```
PASS: All checks passed! You're ready to go.
```

## Security Features

### 1. .gitignore Protection

The following files are protected from git commits:
- `config.py` - Your actual API key
- `.env` - Alternative config method
- `*_api_key.txt` - Any API key text files
- `secrets.py` - Any secrets file

### 2. Template File

`config.example.py` is tracked by git and serves as a template. It contains:
- Structure of config.py
- Placeholder values
- Instructions

Team members can copy this template and add their own keys.

### 3. Multiple Loading Methods

The project tries to load API key from multiple sources (in order):
1. `config.py` (recommended)
2. `.env` file
3. Command line argument `--api-key`

## Usage in Code

### Python Scripts

```python
# Automatically loaded
from config import GEMINI_API_KEY
```

### Jupyter Notebooks

Notebooks automatically import from config.py:
```python
from config import GEMINI_API_KEY
processor = CVProcessor(api_key=GEMINI_API_KEY)
```

### Command Line

```bash
# Uses config.py automatically
python process_new_cv.py my_cv.pdf

# Or override with command line
python process_new_cv.py my_cv.pdf --api-key YOUR_KEY
```

## What NOT to Do

### NEVER commit config.py

```bash
# BAD - DO NOT DO THIS
git add config.py
git commit -m "add config"

# The .gitignore should prevent this, but don't try to force it:
git add -f config.py  # DON'T DO THIS
```

### NEVER hardcode API keys in notebooks

```python
# BAD - visible in git history
GEMINI_API_KEY = "AIzaSyA7yZTVmqEPqrcNkgrcfbJd6pOuQnbukAY"

# GOOD - load from config
from config import GEMINI_API_KEY
```

### NEVER share config.py

- Don't send config.py via email
- Don't include in ZIP files
- Don't screenshot config.py with real keys

## Team Collaboration

### For Team Members

Each team member should:
1. Clone the repository
2. Copy `config.example.py` to `config.py`
3. Add their own Gemini API key
4. Never commit config.py

### For Project Submission

When submitting your project:
1. Make sure config.py is NOT in your ZIP/submission
2. Include config.example.py as template
3. Document in README that users need to create config.py
4. Mention in presentation that API keys are properly secured

## Troubleshooting

### "No API key found" error

Run verification:
```bash
python check_setup.py
```

Check that:
1. config.py exists
2. API key is set (not "YOUR_API_KEY_HERE")
3. No syntax errors in config.py

### config.py appears in git status

This shouldn't happen if .gitignore is correct. Verify:
```bash
# Should show that config.py is ignored
git check-ignore -v config.py

# Should output something like:
# .gitignore:148:config.py    config.py
```

If it's not ignored:
```bash
# Remove from git tracking (if accidentally added)
git rm --cached config.py

# Verify .gitignore contains config.py
grep "config.py" .gitignore
```

### API key visible in notebook outputs

Clear notebook outputs before committing:
```bash
# In Jupyter: Cell > All Output > Clear

# Or using command line:
jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
```

## Alternative: Using .env File

If you prefer using .env instead of config.py:

1. Create .env file:
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

2. Install python-dotenv:
```bash
pip install python-dotenv
```

3. Scripts will automatically try .env if config.py is not found

## Best Practices

1. Use separate API keys for development and production
2. Rotate API keys periodically
3. Don't use personal API keys for team projects
4. Monitor API usage in Google AI Studio
5. Delete unused API keys

## Summary

- config.py stores your API key
- Protected by .gitignore
- Automatically loaded by all scripts
- Never committed to git
- Each team member uses their own key
- Verification script checks setup

For questions, see SETUP.md or run `python check_setup.py`
