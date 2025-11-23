"""
CV Processor - PDF to Dataset and Evaluation Metrics

This module:
1. Extracts text from PDF CVs
2. Adds them to the dataset
3. Generates critiques with all three models
4. Calculates Precision, Recall, and F1 scores for critique quality
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import re

# PDF processing
try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "PyPDF2"])
    import PyPDF2

# Optional: better PDF extraction
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False
    print("Note: pdfplumber not available. Using PyPDF2 (may have lower quality extraction)")
    print("Install with: pip install pdfplumber")

# LLM API
try:
    import google.generativeai as genai
except ImportError:
    print("google-generativeai not installed. Run: pip install google-generativeai")
    genai = None


class CVProcessor:
    """Process PDF CVs and add to dataset with critique generation"""

    # Define common CV issues to detect (for precision/recall calculation)
    EXPECTED_CV_ELEMENTS = {
        'career_objective': ['career objective', 'objective', 'summary', 'professional summary'],
        'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
        'education': ['education', 'academic', 'degree', 'university', 'college'],
        'experience': ['experience', 'work history', 'employment', 'professional experience'],
        'contact': ['email', 'phone', 'address', 'contact', 'linkedin'],
        'achievements': ['achievement', 'award', 'accomplishment', 'certification'],
        'projects': ['project', 'portfolio'],
    }

    COMMON_CV_ISSUES = {
        'typos': ['typo', 'spelling', 'grammar', 'grammatical'],
        'vague_objective': ['vague', 'generic', 'unclear objective', 'bland objective'],
        'skill_organization': ['organize skills', 'categorize skills', 'skill structure'],
        'no_metrics': ['quantif', 'metric', 'number', 'measurable', 'achievement'],
        'buzzwords': ['buzzword', 'cliché', 'jargon', 'overused'],
        'formatting': ['format', 'layout', 'structure', 'consistency'],
        'length': ['too long', 'too short', 'concise', 'verbose'],
        'relevance': ['relevant', 'irrelevant', 'focus'],
    }

    def __init__(self, api_key: str = None):
        """
        Initialize CV Processor

        Args:
            api_key: Gemini API key for critique generation
        """
        self.api_key = api_key
        if api_key and genai:
            genai.configure(api_key=api_key)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Try pdfplumber first (better quality)
        if HAS_PDFPLUMBER:
            try:
                text = self._extract_with_pdfplumber(pdf_path)
                if text.strip():
                    return text
            except Exception as e:
                print(f"pdfplumber failed: {e}. Falling back to PyPDF2")

        # Fallback to PyPDF2
        return self._extract_with_pypdf2(pdf_path)

    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber"""
        import pdfplumber

        text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)

        return "\n\n".join(text)

    def _extract_with_pypdf2(self, pdf_path: Path) -> str:
        """Extract text using PyPDF2"""
        text = []

        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)

        return "\n\n".join(text)

    def parse_cv_text(self, cv_text: str) -> Dict:
        """
        Parse CV text into structured format matching dataset schema

        Args:
            cv_text: Raw CV text

        Returns:
            Dictionary with parsed CV data
        """
        # Simple parsing - extract sections based on common headers
        cv_data = {
            'career_objective': self._extract_section(cv_text, ['objective', 'summary', 'profile']),
            'skills': self._extract_section(cv_text, ['skills', 'technical skills', 'competencies']),
            'educational_institution_name': self._extract_section(cv_text, ['education', 'academic background']),
            'professional_company_names': self._extract_section(cv_text, ['experience', 'work history', 'employment']),
            'certifications': self._extract_section(cv_text, ['certification', 'licenses']),
            'projects': self._extract_section(cv_text, ['projects', 'portfolio']),
            'raw_text': cv_text,
            'extracted_date': datetime.now().isoformat(),
        }

        return cv_data

    def _extract_section(self, text: str, keywords: List[str]) -> str:
        """
        Extract section from CV text based on keywords

        Args:
            text: CV text
            keywords: Section header keywords to search for

        Returns:
            Extracted section text or empty string
        """
        text_lower = text.lower()

        for keyword in keywords:
            # Find section header
            pattern = rf'\b{re.escape(keyword)}\b.*?(?=\n[A-Z][a-z]+:|\n[A-Z][A-Z\s]+\n|$)'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

            if match:
                section_text = match.group(0)
                # Clean up
                section_text = re.sub(rf'^{re.escape(keyword)}:?\s*', '', section_text, flags=re.IGNORECASE)
                return section_text.strip()

        return ""

    def add_to_dataset(self, cv_data: Dict, output_path: str = "data/new_cvs.csv"):
        """
        Add parsed CV to dataset

        Args:
            cv_data: Parsed CV dictionary
            output_path: Path to save/append data
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create DataFrame
        df_new = pd.DataFrame([cv_data])

        # Append or create
        if output_path.exists():
            df_existing = pd.read_csv(output_path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(output_path, index=False)
            print(f" Added CV to existing dataset: {output_path}")
        else:
            df_new.to_csv(output_path, index=False)
            print(f" Created new dataset: {output_path}")

        return output_path

    def generate_critiques(self, cv_text: str) -> Dict[str, str]:
        """
        Generate critiques with all three models

        Args:
            cv_text: Formatted CV text

        Returns:
            Dictionary with gentle, medium, and brutal critiques
        """
        if not self.api_key or not genai:
            raise ValueError("API key required for critique generation")

        prompts = {
            'gentle': {
                'system': """You are a kind career advisor providing constructive CV feedback.

Structure:  STRENGTHS |  AREAS FOR IMPROVEMENT |  ACTION ITEMS |  FINAL THOUGHTS""",
                'temperature': 0.4
            },
            'medium': {
                'system': """You are an experienced hiring manager providing direct, honest feedback.

Structure:  FIRST IMPRESSION |  MAJOR ISSUES |  CONCERNS |  WHAT WORKS |  BOTTOM LINE""",
                'temperature': 0.7
            },
            'brutal': {
                'system': """You are a savage CV roaster with no filter but clever humor.

Structure:  OPENING ROAST |  CAREER OBJECTIVE AUTOPSY |  SKILLS COMEDY |  EXPERIENCE CHECK |  FATAL FLAWS |  MIC DROP""",
                'temperature': 0.9
            }
        }

        critiques = {}

        for model_name, config in prompts.items():
            print(f"Generating {model_name} critique...")

            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config=genai.GenerationConfig(
                    temperature=config['temperature'],
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=1024,
                )
            )

            full_prompt = f"{config['system']}\n\nReview this CV:\n\n{cv_text}"

            try:
                response = model.generate_content(full_prompt)
                critiques[model_name] = response.text
            except Exception as e:
                print(f"Error generating {model_name} critique: {e}")
                critiques[model_name] = f"Error: {str(e)}"

        return critiques

    def calculate_section_coverage(self, cv_text: str, critique: str) -> Dict[str, float]:
        """
        Calculate what % of CV sections were addressed in critique

        Args:
            cv_text: Original CV text
            critique: Generated critique

        Returns:
            Coverage metrics
        """
        cv_lower = cv_text.lower()
        critique_lower = critique.lower()

        # Check which sections exist in CV
        sections_present = {}
        for section, keywords in self.EXPECTED_CV_ELEMENTS.items():
            sections_present[section] = any(kw in cv_lower for kw in keywords)

        # Check which sections were addressed in critique
        sections_covered = {}
        for section, keywords in self.EXPECTED_CV_ELEMENTS.items():
            sections_covered[section] = any(kw in critique_lower for kw in keywords)

        # Calculate coverage
        total_sections = sum(sections_present.values())
        covered_sections = sum(
            1 for section in sections_present
            if sections_present[section] and sections_covered[section]
        )

        coverage_rate = covered_sections / total_sections if total_sections > 0 else 0

        return {
            'total_sections_in_cv': total_sections,
            'sections_addressed_in_critique': covered_sections,
            'coverage_rate': coverage_rate,
            'sections_present': sections_present,
            'sections_covered': sections_covered,
        }

    def calculate_issue_detection_metrics(self, cv_text: str, critique: str,
                                         ground_truth_issues: List[str] = None) -> Dict[str, float]:
        """
        Calculate Precision, Recall, F1 for issue detection in critique

        This treats the critique as a "detector" of CV issues.

        Args:
            cv_text: Original CV text
            critique: Generated critique
            ground_truth_issues: List of actual issues in the CV
                                If None, we detect potential issues automatically

        Returns:
            Dictionary with precision, recall, F1, and supporting metrics
        """
        critique_lower = critique.lower()
        cv_lower = cv_text.lower()

        # If no ground truth provided, detect potential issues automatically
        if ground_truth_issues is None:
            ground_truth_issues = self._detect_cv_issues(cv_text)

        # Check which issues the critique mentions
        detected_issues = []
        for issue_category, keywords in self.COMMON_CV_ISSUES.items():
            if any(kw in critique_lower for kw in keywords):
                detected_issues.append(issue_category)

        # Calculate metrics
        true_positives = len(set(ground_truth_issues) & set(detected_issues))
        false_positives = len(set(detected_issues) - set(ground_truth_issues))
        false_negatives = len(set(ground_truth_issues) - set(detected_issues))

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'ground_truth_issues': ground_truth_issues,
            'detected_issues': detected_issues,
            'missed_issues': list(set(ground_truth_issues) - set(detected_issues)),
            'extra_mentions': list(set(detected_issues) - set(ground_truth_issues)),
        }

    def _detect_cv_issues(self, cv_text: str) -> List[str]:
        """
        Automatically detect potential issues in CV

        Args:
            cv_text: CV text to analyze

        Returns:
            List of detected issue categories
        """
        issues = []
        cv_lower = cv_text.lower()

        # Check for common issues

        # Vague objective - contains generic words
        if any(word in cv_lower for word in ['seeking', 'looking for', 'opportunity']):
            if not any(word in cv_lower for word in ['specific', 'specialize', 'expert in']):
                issues.append('vague_objective')

        # No metrics - lacks numbers
        if not re.search(r'\d+%|\d+x|increased|reduced|improved \d+', cv_text):
            issues.append('no_metrics')

        # Buzzwords
        buzzwords = ['synergy', 'innovative', 'dynamic', 'results-driven', 'team player', 'hard worker']
        if sum(1 for bw in buzzwords if bw in cv_lower) >= 2:
            issues.append('buzzwords')

        # Length issues
        word_count = len(cv_text.split())
        if word_count < 200:
            issues.append('length')
        elif word_count > 1000:
            issues.append('length')

        # Missing sections
        has_skills = any(kw in cv_lower for kw in self.EXPECTED_CV_ELEMENTS['skills'])
        has_experience = any(kw in cv_lower for kw in self.EXPECTED_CV_ELEMENTS['experience'])

        if not has_skills or not has_experience:
            issues.append('formatting')

        return issues

    def evaluate_all_models(self, cv_text: str, critiques: Dict[str, str],
                           ground_truth_issues: List[str] = None) -> pd.DataFrame:
        """
        Evaluate all three models with comprehensive metrics

        Args:
            cv_text: Original CV text
            critiques: Dictionary of critiques from all models
            ground_truth_issues: Optional list of actual issues

        Returns:
            DataFrame with evaluation results
        """
        results = []

        for model_name, critique in critiques.items():
            # Coverage metrics
            coverage = self.calculate_section_coverage(cv_text, critique)

            # Issue detection metrics (Precision, Recall, F1)
            detection = self.calculate_issue_detection_metrics(cv_text, critique, ground_truth_issues)

            # Combine metrics
            result = {
                'model': model_name,
                'coverage_rate': coverage['coverage_rate'],
                'sections_addressed': coverage['sections_addressed_in_critique'],
                'precision': detection['precision'],
                'recall': detection['recall'],
                'f1_score': detection['f1_score'],
                'true_positives': detection['true_positives'],
                'false_positives': detection['false_positives'],
                'false_negatives': detection['false_negatives'],
                'critique_length': len(critique.split()),
            }

            results.append(result)

        return pd.DataFrame(results)


def main():
    """Example usage"""

    print("="*80)
    print("CV PROCESSOR - PDF to Dataset with Evaluation Metrics")
    print("="*80)

    # Configuration
    PDF_PATH = "path/to/your/cv.pdf"  # Change this
    API_KEY = "YOUR_API_KEY_HERE"  # Change this

    # Initialize processor
    processor = CVProcessor(api_key=API_KEY)

    # Example 1: Extract and add CV to dataset
    print("\n1. EXTRACTING CV FROM PDF...")
    print("-"*80)

    try:
        # Extract text
        cv_text = processor.extract_text_from_pdf(PDF_PATH)
        print(f" Extracted {len(cv_text)} characters")
        print(f"Preview: {cv_text[:200]}...\n")

        # Parse into structured format
        cv_data = processor.parse_cv_text(cv_text)
        print(f" Parsed CV sections")

        # Add to dataset
        dataset_path = processor.add_to_dataset(cv_data)
        print(f" Added to dataset: {dataset_path}\n")

    except FileNotFoundError:
        print(f"  PDF not found: {PDF_PATH}")
        print("Using sample text for demonstration...\n")

        cv_text = """
        CAREER OBJECTIVE:
        Seeking a challenging position in data science.

        SKILLS:
        Python, Machine Learning, Data Analysis

        EDUCATION:
        University of Example - B.Sc. Computer Science (2020)

        WORK EXPERIENCE:
        Data Analyst at Company XYZ (2020-Present)
        - Analyzed data
        - Created reports
        - Worked with team
        """

    # Example 2: Generate critiques
    print("\n2. GENERATING CRITIQUES...")
    print("-"*80)

    if API_KEY != "YOUR_API_KEY_HERE":
        critiques = processor.generate_critiques(cv_text)

        for model_name, critique in critiques.items():
            print(f"\n{model_name.upper()} CRITIQUE:")
            print(critique[:300] + "...\n")
    else:
        print("  API key not configured. Skipping critique generation.")
        # Use mock critiques for demo
        critiques = {
            'gentle': "Your CV shows good foundation. Consider adding metrics to quantify achievements.",
            'medium': "Missing quantifiable results. Experience section is too vague. Skills need organization.",
            'brutal': "Generic buzzwords everywhere. 'Analyzed data' - what data? How? This needs metrics."
        }

    # Example 3: Calculate metrics
    print("\n3. CALCULATING EVALUATION METRICS...")
    print("-"*80)

    # Evaluate all models
    df_results = processor.evaluate_all_models(cv_text, critiques)

    print("\n EVALUATION RESULTS:")
    print(df_results.to_string(index=False))

    # Detailed breakdown for one model
    print("\n\n4. DETAILED METRICS FOR MEDIUM MODEL:")
    print("-"*80)

    detection = processor.calculate_issue_detection_metrics(cv_text, critiques['medium'])

    print(f"Precision: {detection['precision']:.2%}")
    print(f"Recall: {detection['recall']:.2%}")
    print(f"F1 Score: {detection['f1_score']:.2%}")
    print(f"\nTrue Positives: {detection['true_positives']}")
    print(f"False Positives: {detection['false_positives']}")
    print(f"False Negatives: {detection['false_negatives']}")
    print(f"\nGround Truth Issues: {detection['ground_truth_issues']}")
    print(f"Detected Issues: {detection['detected_issues']}")
    print(f"Missed Issues: {detection['missed_issues']}")

    # Coverage metrics
    coverage = processor.calculate_section_coverage(cv_text, critiques['medium'])
    print(f"\nSection Coverage: {coverage['coverage_rate']:.2%}")
    print(f"Sections Addressed: {coverage['sections_addressed_in_critique']}/{coverage['total_sections_in_cv']}")

    print("\n" + "="*80)
    print(" PROCESSING COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
