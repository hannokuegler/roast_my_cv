#  Roast My CV - Setup Guide

This guide will help you set up and run the CV roasting project.

##  Prerequisites

- Python 3.11 or higher
- Gemini API key (free tier available)
- Jupyter Notebook

##  Quick Start

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy your API key

### 2. Configure API Key (IMPORTANT - Do this FIRST)

The project automatically loads your API key from config.py.

**Option A: Use config.py (Recommended - Most Secure)**

1. Copy the example config file:
```bash
cp config.example.py config.py
```

2. Edit config.py and add your actual API key:
```python
GEMINI_API_KEY = "your_actual_api_key_here"
```

**Security Note:** config.py is listed in .gitignore and will NEVER be committed to git, keeping your API key safe.

**Option B: Use .env file**
```bash
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

The .env file is also protected by .gitignore.

### 3. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 4. OLD Method (Not Recommended)
# Copy the example file
cp .env.example .env

# Edit .env and add your key
echo "GEMINI_API_KEY=your_actual_key_here" > .env
```

Then in notebooks, load it:
```python
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

### 4. Run the Notebooks

Execute notebooks in order:

```bash
jupyter notebook
```

Then run:
1. **01_eda.ipynb** - Explore the data
2. **02_gentle_roaster.ipynb** - Generate gentle critiques
3. **03_medium_roaster.ipynb** - Generate medium critiques
4. **04_brutal_roaster.ipynb** - Generate brutal roasts
5. **05_evaluation_comparison.ipynb** - Compare all models

##  Project Structure

```
roast_my_cv/
 data/
    resume_data.csv          # Resume dataset
    test_cv_indices.json     # Test CV selection (auto-generated)
 notebooks/
    01_eda.ipynb             # Data exploration
    02_gentle_roaster.ipynb  # Gentle model
    03_medium_roaster.ipynb  # Medium model
    04_brutal_roaster.ipynb  # Brutal model
    05_evaluation_comparison.ipynb  # Comparison
 results/
    gentle_roaster/          # Gentle results
    medium_roaster/          # Medium results
    brutal_roaster/          # Brutal results
    model_comparison.png     # Visualizations (auto-generated)
    summary_report.json      # Final report (auto-generated)
 requirements.txt             # Dependencies
 .env.example                 # API key template
 SETUP.md                     # This file
```

##  Usage Examples

### Running Individual Notebooks

Each notebook is self-contained. Simply:
1. Open the notebook in Jupyter
2. Run all cells (Cell → Run All)
3. Check the `results/` folder for outputs

### Customizing Temperature

In each roaster notebook, you can experiment with different temperatures:

```python
# In the notebook
OPTIMAL_TEMPERATURE = 0.7  # Change this value (0.0 - 1.0)
```

- **Lower (0.1-0.4)**: More focused, consistent, conservative
- **Medium (0.5-0.7)**: Balanced creativity and consistency
- **Higher (0.8-1.0)**: More creative, varied, unpredictable

### Testing Different CVs

To test with different CVs:

1. Open `01_eda.ipynb`
2. Modify this cell:
```python
# Select different CV indices
test_cv_indices = [0, 5]  # Change these numbers
```
3. Re-run notebooks 02-04

##  Troubleshooting

### "API Key Error"
- Make sure you've replaced `YOUR_API_KEY_HERE` with your actual key
- Check that your API key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Ensure you've enabled the Generative AI API

### "Module not found"
```bash
# Make sure you've installed all dependencies
pip install -r requirements.txt
```

### "No results found"
- Make sure you've run notebooks 02-04 first
- Check that results are being saved to the correct folders
- Verify the `results/` folders exist

### Rate Limiting
If you hit rate limits:
- Add delays between API calls
- Use the free tier responsibly
- Consider upgrading to paid tier for higher limits

##  Tips

1. **Start with EDA**: Always run notebook 01 first to understand your data
2. **One at a time**: Run notebooks sequentially, not all at once
3. **Check outputs**: After each notebook, verify results are saved
4. **Experiment**: Try different temperatures and prompts
5. **Save API calls**: Results are cached, so you don't need to regenerate

##  Understanding Results

After running all notebooks, you'll have:

- **JSON files**: Detailed results for each CV and model
- **Visualizations**: Charts comparing model performance
- **Summary report**: Overall statistics and findings

##  Learning Objectives

This project demonstrates:

1. **Prompt Engineering**: Creating different tones with prompts alone
2. **Temperature Tuning**: How temperature affects output creativity
3. **LLM Evaluation**: Using one LLM to judge another
4. **Practical ML**: Building useful applications without fine-tuning

##  Need Help?

- Check the course Canvas page
- Review the notebook markdown cells for explanations
- Look at example outputs in the `results/` folder
- Ask your instructor or TAs

##  Important Notes

- **API Costs**: Gemini Flash has a free tier, but be mindful of usage
- **Data Privacy**: Don't use real personal CVs without consent
- **Ethical Use**: The brutal roaster is for entertainment/education only
- **Academic Integrity**: This is a learning tool - understand the code!

---

**Happy Roasting!** 
