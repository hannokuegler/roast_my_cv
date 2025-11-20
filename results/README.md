# Results Directory

This directory contains the outputs from all three CV roasting models.

## Structure

```
results/
├── gentle_roaster/       # Gentle, constructive feedback
│   ├── cv_0_gentle.json
│   └── cv_1_gentle.json
├── medium_roaster/       # Direct, honest critiques
│   ├── cv_0_medium.json
│   └── cv_1_medium.json
├── brutal_roaster/       # Savage, humorous roasts
│   ├── cv_0_brutal.json
│   └── cv_1_brutal.json
├── model_comparison.png  # Visual comparison
├── temperature_analysis.png  # Temperature effects
├── evaluation_scores.png     # Quality scores
└── summary_report.json   # Overall statistics
```

## File Format

Each result file contains:

```json
{
  "cv_index": 0,
  "model": "gentle_roaster",
  "temperature": 0.4,
  "timestamp": "2024-01-01T12:00:00",
  "cv_text": "Original CV content...",
  "critique": "Generated critique..."
}
```

## How Results are Generated

1. Run `02_gentle_roaster.ipynb` → generates gentle critiques
2. Run `03_medium_roaster.ipynb` → generates medium critiques
3. Run `04_brutal_roaster.ipynb` → generates brutal roasts
4. Run `05_evaluation_comparison.ipynb` → creates visualizations and summary

## Viewing Results

Results can be viewed:
- **In Jupyter**: Notebooks display results inline
- **As JSON**: Open `.json` files in any text editor
- **As Images**: View the `.png` charts
- **In Summary**: Check `summary_report.json` for statistics
