# Roast My CV - LLM Project

This is a Machine Learning project using LLMs to critique CVs with three different styles (Gentle, Medium, Brutal).

## Quick Start

1. **Get Gemini API Key**: https://makersuite.google.com/app/apikey

2. **Configure API Key**:
```bash
cp config.example.py config.py
# Edit config.py and add your API key
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run Interactive Notebook**:
```bash
jupyter notebook notebooks/06_quick_cv_roaster_v2.ipynb
```

## Features

- Three roaster models: Gentle, Medium, Brutal
- Temperature tuning experiments
- Precision, Recall, F1 evaluation metrics
- PDF CV processing
- Automated evaluation with LLM-as-judge

## Documentation

- **SETUP.md** - Full installation guide
- **USAGE_GUIDE.md** - How to use with "Command Line Script" and "Python API". Desription and Interpretation of the metrics
- **PROJECT_SUMMARY.md** - Project overview

## Security

- API keys are stored in `config.py` (not committed to git)
- `.gitignore` protects sensitive files
- Use `config.example.py` as template
