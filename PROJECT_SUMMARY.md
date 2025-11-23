#  Roast My CV - Project Summary

## Project Components

###  Notebooks (6 total)

1. **01_eda.ipynb** - Exploratory Data Analysis
   - Loads and explores the resume dataset
   - Creates helper functions for formatting CVs
   - Provides data quality insights

2. **02_gentle_roaster.ipynb** - Gentle Roaster
   - Constructive, encouraging feedback
   - Professional and supportive tone
   - Temperature experiments

3. **03_medium_roaster.ipynb** - Medium Roaster
   - Direct, honest feedback
   - Balanced criticism
   - Temperature experiments

4. **04_brutal_roaster.ipynb** - Brutal Roaster
   - Savage, humorous roasts
   - Maximum creativity
   - Temperature experiments

5. **05_evaluation_comparison.ipynb** - Evaluation & Comparison
   - Side-by-side comparison of all models
   - Quantitative analysis (word count, length, etc.)
   - LLM-based quality evaluation

6. **06_quick_cv_roaster_v2.ipynb** - Quick CV Roasting Application
- CV Input (PDF upload or dataset sample)
- Automatic text extraction & preprocessing
- Model selection to generate output
- Evaluation metrics (precision, recall, F1, coverage)



###  Directory Structure

```
roast_my_cv/
 data/
    cv_texts.txt  
    resume_data.csv
    test_cv_indices.json              
 notebooks/
    01_eda.ipynb                   
    02_gentle_roaster.ipynb        
    03_medium_roaster.ipynb        
    04_brutal_roaster.ipynb        
    05_evaluation_comparison.ipynb
    06_quick_cv_roaster_v2.ipynb  
 results/
    gentle_roaster/              # Will contain gentle critiques
       SAMPLE_cv_0_gentle.json  #  Sample file created
    medium_roaster/              # Will contain medium critiques
       SAMPLE_cv_0_medium.json  #  Sample file created
    brutal_roaster/              # Will contain brutal roasts
       SAMPLE_cv_0_brutal.json  #  Sample file created
 README.md                          
 requirements.txt                 #  Dependencies listed
 .env.example                     #  API key template
 SETUP.md                         #  Setup instructions
 PROJECT_SUMMARY.md               #  This file
 USAGE_Guide.md                   #  Including instructions for automated usage
```

##  Key Features Implemented

### 1. **Temperature Tuning**
- **Gentle**: T=0.4 (focused)
- **Medium**: T=0.7 (balanced)
- **Brutal**: T=0.9 (creative)

### 2. **Prompt Engineering**
Three different prompts:
- Gentle: Supportive career advisor
- Medium: Experienced hiring manager
- Brutal: Savage roast comedian

### 3. **Scalable Code**
- Reusable functions for CV formatting
- JSON output for easy processing
- Clear, modular notebook structure


##  Next Steps - What YOU Need to Do

### Step 1: Get Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create/get your free API key
3. Copy it

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key
Open each notebook (02, 03, 04, 05) and replace:
```python
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```
With your actual key.

### Step 4: Run Notebooks in Order
```bash
jupyter notebook
```

Run notebooks sequentially:
1. 01_eda.ipynb
2. 02_gentle_roaster.ipynb
3. 03_medium_roaster.ipynb
4. 04_brutal_roaster.ipynb
5. 05_evaluation_comparison.ipynb
6. 06_quick_cv_roaster_v2.ipynb

### Step 5: Review Results
Check the `results/` folder for:
- JSON files with critiques
- PNG visualizations
- summary_report.json

##  What You'll Get

After running all notebooks:

1. **CV Critiques**
2. **Temperature Analysis** showing effects of different settings
3. **Quality Scores** from LLM judge
4. **Summary Report** with all statistics

##  Learning Outcomes

This project demonstrates:

1.  **Prompt Engineering**: Creating different tones without fine-tuning
2.  **Temperature Tuning**: Controlling output creativity
3.  **LLM APIs**: Working with Gemini API
4.  **Evaluation**: Using LLMs to judge other LLMs
5.  **Data Analysis**: Quantitative comparison of models
6.  **Visualization**: Creating informative charts

##  Tips for Success

1. **Start Small**: Run notebook 01 first to understand the data
2. **One at a Time**: Don't run all notebooks at once
3. **Check Outputs**: Verify results are saved after each notebook
4. **Experiment**: Try different temperatures and prompts
5. **Document**: Add your own observations in markdown cells
6. **Save API Calls**: Results are cached - no need to regenerate

##  Customization Options

### Change Test CVs
In `01_eda.ipynb`:
```python
test_cv_indices = [0, 1]  # Change to [2, 5] or any other indices
```

### Adjust Temperatures
In roaster notebooks:
```python
OPTIMAL_TEMPERATURE = 0.7  # Try different values
```

### Modify Prompts
Edit the system prompts in notebooks 02-04 to change the tone:
```python
GENTLE_SYSTEM_PROMPT = """Your custom prompt here..."""
```

##  Troubleshooting

**Problem**: "API Key Error"
- Solution: Make sure you've replaced YOUR_API_KEY_HERE with your actual key

**Problem**: "Module not found"
- Solution: Run `pip install -r requirements.txt`

**Problem**: "No results found"
- Solution: Run notebooks 02-04 first to generate results

**Problem**: Rate limiting
- Solution: Add `time.sleep(2)` between API calls
