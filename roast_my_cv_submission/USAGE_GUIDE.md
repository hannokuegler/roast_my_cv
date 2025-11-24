#  Usage Guide - CV Roaster with Metrics

## Prerequisites

Make sure you've configured your API key first:

```bash
# Copy example config and add your API key
cp config.example.py config.py
# Edit config.py and set GEMINI_API_KEY

# Verify setup
python check_setup.py
```

## Quick Start

### Method 1: Interactive Jupyter Notebook (Recommended)

The easiest way to test your CV roasters:

```bash
jupyter notebook notebooks/06_quick_cv_roaster_v2.ipynb
```

**Features:**
-  Automatically loads API key from config.py
-  Upload PDF CV(s) or select from dataset
-  Choose roaster model (Gentle/Medium/Brutal)
-  Get instant metrics (Precision, Recall, F1)
-  Save results automatically

**Steps:**
1. Configure API key in config.py (one-time setup)
2. Open the notebook "06_quick_cv_roaster_v2.ipynb"
3. Upload a PDF CV OR select from dataset
4. Choose roaster style
5. Click "Run All" to generate roast + metrics

---

### Method 2: Command Line Script

Process PDFs from terminal:

```bash
python process_new_cv.py path/to/cv.pdf --api-key YOUR_KEY
```

**Options:**
```bash
# Basic usage
python process_new_cv.py my_cv.pdf

# Custom output location
python process_new_cv.py my_cv.pdf --output data/my_cvs.csv

# Save critiques to specific folder
python process_new_cv.py my_cv.pdf --save-critiques results/my_tests/
```

**What it does:**
1. Extracts text from PDF
2. Adds to dataset
3. Generates all 3 roasts (gentle/medium/brutal)
4. Calculates metrics
5. Saves everything

---

### Method 3: Python API

Use in your own scripts:

```python
from cv_processor import CVProcessor

# Initialize
processor = CVProcessor(api_key="YOUR_API_KEY")

# Extract from PDF
cv_text = processor.extract_text_from_pdf("cv.pdf")

# Generate critiques
critiques = processor.generate_critiques(cv_text)

# Get metrics
df_metrics = processor.evaluate_all_models(cv_text, critiques)
print(df_metrics)

# Get detailed analysis for one model
detection = processor.calculate_issue_detection_metrics(
    cv_text,
    critiques['medium']
)

print(f"Precision: {detection['precision']:.2%}")
print(f"Recall: {detection['recall']:.2%}")
print(f"F1 Score: {detection['f1_score']:.2%}")
```

---

##  Understanding the Metrics

### Precision, Recall, and F1 Score

These metrics evaluate how well the roaster identifies CV issues:

**Precision** - "Accuracy of critique" *Of all issues mentioned in critique, what % are real issues?*
- Formula: `True Positives / (True Positives + False Positives)` 
- **High precision (>0.8)** = Critique is accurate
- **Low precision (<0.5)** = Critique mentions many non-existent issues

**Recall** - "Completeness of critique" *Of all actual issues in CV, what % did critique catch?*
- Formula: `True Positives / (True Positives + False Negatives)` 
- **High recall (>0.8)** = Critique is comprehensive
- **Low recall (<0.5)** = Critique misses many actual problems

**F1 Score** - "Overall quality" *Balanced measure of both precision and recall*
- Formula: `2 × (Precision × Recall) / (Precision + Recall)`
- **High F1 (>0.7)** = Good overall critique quality
- **Low F1 (<0.5)** = Needs improvement

**Example:**

```
CV has 5 actual issues: [vague_objective, no_metrics, buzzwords, formatting, length]

Critique mentions 4 issues: [vague_objective, no_metrics, buzzwords, typos]

Analysis:
- True Positives (TP) = 3 (vague_objective, no_metrics, buzzwords)
- False Positives (FP) = 1 (typos - not actually in CV)
- False Negatives (FN) = 2 (formatting, length - missed by critique)

Precision = 3/(3+1) = 0.75 (75% accuracy)
Recall = 3/(3+2) = 0.60 (60% coverage)
F1 = 2×(0.75×0.60)/(0.75+0.60) = 0.67
```

---

### Coverage Rate

**Coverage** - "Section thoroughness"
- Question: *What % of CV sections were addressed?*
- Checks if critique mentions: objective, skills, education, experience, etc.
- **High coverage (>0.8)** = Thorough analysis
- **Low coverage (<0.5)** = Incomplete review

---

##  What Makes a Good Roaster?

| Metric | Gentle | Medium | Brutal | Ideal |
|--------|--------|--------|--------|-------|
| **Precision** | High (0.8+) | Medium-High (0.7+) | Medium (0.6+) | 0.7+ |
| **Recall** | Medium (0.6+) | High (0.8+) | Medium (0.6+) | 0.7+ |
| **F1 Score** | 0.7+ | 0.75+ | 0.6+ | 0.7+ |
| **Coverage** | High (0.8+) | High (0.8+) | Medium (0.6+) | 0.7+ |

**Why differences?**
- **Gentle**: Should be accurate (high precision) but might soften criticism (medium recall)
- **Medium**: Should catch everything (high recall) and be accurate (high precision)
- **Brutal**: Creative/humorous, may exaggerate (lower precision), entertainment > completeness

---

##  Interpreting Your Results

### Strong Results 
```
Model: medium
Precision: 0.85 (85%)
Recall: 0.90 (90%)
F1 Score: 0.87 (87%)
Coverage: 0.92 (92%)

→ Excellent! Accurate, comprehensive, and thorough
```

### Needs Improvement 
```
Model: brutal
Precision: 0.45 (45%)
Recall: 0.50 (50%)
F1 Score: 0.47 (47%)
Coverage: 0.60 (60%)

→ Poor quality - making up issues or missing real ones
```

### How to Improve:
1. **Low Precision** → Adjust prompt to be more specific
2. **Low Recall** → Add more examples to increase context
3. **Low Coverage** → Explicitly instruct to review all sections
4. **All low** → Rethink prompt strategy and/or try different temperature

---

##  Tips

### For Best Results:
1. **Use high-quality PDF CVs** - Clear text, good formatting
2. **Test multiple models** - Compare gentle/medium/brutal
3. **Review ground truth** - Recheck if auto-detected issues are accurate
4. **Iterate prompts** - Use metrics to improve your prompts
5. **Document findings** - Save results

### Common Combined Issues:

**"Low F1 scores across all models"**
- Check CV quality, is it complete enough to evaluate?
- Consider if issues are too subjective

**"High precision but low recall"**
- Add instruction to check all sections
- Increase max_output_tokens for longer critiques

**"High recall but low precision"**
- Make prompts more specific
- Lower temperature for more focused output

---

##  File Outputs

After processing, you'll get:

```
results/
 quick_tests/
    critique_gentle_20241120_153045.txt
    critique_medium_20241120_153045.txt
    critique_brutal_20241120_153045.txt
    metrics_20241120_153045.json
 new_cv_critiques/
     my_cv_gentle.txt
     my_cv_medium.txt
     my_cv_brutal.txt
     my_cv_metrics.json
```

**metrics.json structure:**
```json
[
  {
    "model": "medium",
    "precision": 0.85,
    "recall": 0.90,
    "f1_score": 0.87,
    "coverage_rate": 0.92,
    "true_positives": 4,
    "false_positives": 1,
    "false_negatives": 1,
    "detected_issues": ["vague_objective", "no_metrics", ...],
    "missed_issues": ["formatting"]
  }
]
```

---

##  Next Steps

1. **Run notebook 06** to test your roasters interactively
2. **Collect metrics** on multiple CVs (5-10 samples)
3. **Compare models** - which works best for your use case?
4. **Document findings** in your project report
5. **Show metrics in presentation** - demonstrates rigorous evaluation

---

##  FAQ

**Q: Can I define custom issues to detect?**
A: Yes! Modify `COMMON_CV_ISSUES` in `cv_processor.py`

**Q: Why are my F1 scores low?**
A: Could be: (1) CV is too short, (2) Auto-detection failed, (3) Model needs prompt tuning

**Q: Which model should have the highest F1?**
A: Medium roaster - it's designed for direct, honest feedback

**Q: Do I need all three metrics?**
A: For ML projects, yes - shows comprehensive evaluation approach

---

##  Inspiration for Your Project Report

Include:

1. **Metrics table** for all three models
2. **Explanation** of what precision/recall/F1 mean in this context
3. **Comparison** - which model performs best and why
4. **Insights** - what did you learn from the metrics?

**Sample write-up:**

> We evaluated our three roaster models using precision, recall, and F1 scores for CV issue detection. The medium roaster achieved the highest F1 score (0.87), demonstrating both accuracy (precision: 0.85) and completeness (recall: 0.90) in identifying CV weaknesses. The gentle roaster showed high precision (0.82) but lower recall (0.68), indicating it accurately identifies issues but may soften criticism. The brutal roaster, while entertaining, showed lower precision (0.62) due to creative exaggeration, which is acceptable given its comedic purpose.

Good luck! 
