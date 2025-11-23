#!/usr/bin/env python3
"""
Simple script to process a new CV PDF and evaluate it

Usage:
    python process_new_cv.py your_cv.pdf

Or with custom API key:
    python process_new_cv.py your_cv.pdf --api-key YOUR_KEY
"""

import sys
import argparse
from pathlib import Path
import json
from cv_processor import CVProcessor


def main():
    parser = argparse.ArgumentParser(description='Process CV PDF and generate critiques with metrics')
    parser.add_argument('pdf_path', type=str, help='Path to CV PDF file')
    parser.add_argument('--api-key', type=str, default=None, help='Gemini API key (or set in .env)')
    parser.add_argument('--output', type=str, default='data/new_cvs.csv', help='Output dataset path')
    parser.add_argument('--save-critiques', type=str, default='results/new_cv_critiques/',
                       help='Directory to save critique results')

    args = parser.parse_args()

    # Get API key - try multiple sources
    api_key = args.api_key

    # Try config.py first
    if not api_key:
        try:
            from config import GEMINI_API_KEY
            api_key = GEMINI_API_KEY
        except ImportError:
            pass

    # Try .env file
    if not api_key:
        try:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
        except ImportError:
            pass

    if not api_key:
        print("  No API key found. Options:")
        print("  1. Add to config.py (recommended)")
        print("  2. Use --api-key argument")
        print("  3. Set in .env file")
        print("Continuing without critique generation...\n")

    # Initialize processor
    processor = CVProcessor(api_key=api_key)

    print("="*80)
    print(f"Processing CV: {args.pdf_path}")
    print("="*80)

    # Step 1: Extract text from PDF
    print("\n Step 1: Extracting text from PDF...")
    try:
        cv_text = processor.extract_text_from_pdf(args.pdf_path)
        print(f" Extracted {len(cv_text)} characters")
        print(f"\nPreview:\n{cv_text[:300]}...\n")
    except Exception as e:
        print(f" Error extracting PDF: {e}")
        sys.exit(1)

    # Step 2: Parse CV structure
    print("\n Step 2: Parsing CV structure...")
    cv_data = processor.parse_cv_text(cv_text)
    print(f" Identified sections:")
    for key, value in cv_data.items():
        if value and key not in ['raw_text', 'extracted_date']:
            preview = value[:50] + "..." if len(value) > 50 else value
            print(f"   - {key}: {preview}")

    # Step 3: Add to dataset
    print(f"\n Step 3: Adding to dataset...")
    dataset_path = processor.add_to_dataset(cv_data, args.output)
    print(f" Dataset updated: {dataset_path}")

    # Step 4: Generate critiques (if API key available)
    if api_key:
        print("\n Step 4: Generating critiques with all models...")
        try:
            critiques = processor.generate_critiques(cv_text)
            print(" Generated critiques from all models\n")

            # Save critiques
            save_dir = Path(args.save_critiques)
            save_dir.mkdir(parents=True, exist_ok=True)

            cv_filename = Path(args.pdf_path).stem
            for model_name, critique in critiques.items():
                output_file = save_dir / f"{cv_filename}_{model_name}.txt"
                with open(output_file, 'w') as f:
                    f.write(critique)
                print(f"   Saved: {output_file}")

        except Exception as e:
            print(f" Error generating critiques: {e}")
            critiques = None
    else:
        print("\n⏭  Step 4: Skipping critique generation (no API key)")
        critiques = None

    # Step 5: Calculate metrics
    print("\n Step 5: Calculating evaluation metrics...")

    if critiques:
        # Evaluate all models
        df_results = processor.evaluate_all_models(cv_text, critiques)

        print("\n" + "="*80)
        print("EVALUATION RESULTS - ALL MODELS")
        print("="*80)
        print(df_results.to_string(index=False))
        print("\n")

        # Save results
        results_file = save_dir / f"{cv_filename}_metrics.json"
        results_dict = df_results.to_dict('records')

        # Add detailed analysis for each model
        for model_name, critique in critiques.items():
            detection = processor.calculate_issue_detection_metrics(cv_text, critique)
            coverage = processor.calculate_section_coverage(cv_text, critique)

            model_result = next(r for r in results_dict if r['model'] == model_name)
            model_result.update({
                'detailed_detection': detection,
                'detailed_coverage': coverage,
                'critique_preview': critique[:200]
            })

        with open(results_file, 'w') as f:
            json.dump(results_dict, f, indent=2)

        print(f" Detailed metrics saved to: {results_file}")

        # Print detailed analysis for best model
        best_model_row = df_results.loc[df_results['f1_score'].idxmax()]
        best_model = best_model_row['model']

        print("\n" + "="*80)
        print(f"DETAILED ANALYSIS - {best_model.upper()} MODEL (Best F1)")
        print("="*80)

        detection = processor.calculate_issue_detection_metrics(cv_text, critiques[best_model])

        print(f"\n Issue Detection Metrics:")
        print(f"   Precision: {detection['precision']:.2%} - How accurate are the critique's issue identifications")
        print(f"   Recall:    {detection['recall']:.2%} - What % of actual issues were identified")
        print(f"   F1 Score:  {detection['f1_score']:.2%} - Overall balance of precision and recall")

        print(f"\n Confusion Matrix:")
        print(f"   True Positives:  {detection['true_positives']} - Issues correctly identified")
        print(f"   False Positives: {detection['false_positives']} - Issues mentioned that don't exist")
        print(f"   False Negatives: {detection['false_negatives']} - Issues missed by critique")

        print(f"\n Issue Breakdown:")
        print(f"   Ground Truth (actual issues):  {detection['ground_truth_issues']}")
        print(f"   Detected (mentioned in critique): {detection['detected_issues']}")
        if detection['missed_issues']:
            print(f"     Missed: {detection['missed_issues']}")
        if detection['extra_mentions']:
            print(f"   ℹ  Extra mentions: {detection['extra_mentions']}")

        coverage = processor.calculate_section_coverage(cv_text, critiques[best_model])
        print(f"\n Section Coverage:")
        print(f"   Coverage Rate: {coverage['coverage_rate']:.2%}")
        print(f"   Sections Addressed: {coverage['sections_addressed_in_critique']}/{coverage['total_sections_in_cv']}")

    else:
        # Just show what issues exist in the CV
        print("\nDetected CV issues (without critique comparison):")
        issues = processor._detect_cv_issues(cv_text)
        for issue in issues:
            print(f"   - {issue}")

    print("\n" + "="*80)
    print(" PROCESSING COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
