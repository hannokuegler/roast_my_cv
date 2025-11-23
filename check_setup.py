#!/usr/bin/env python3
"""
Quick setup verification script.
Run this to check if your API key is configured correctly.
"""

import sys
from pathlib import Path

def check_setup():
    """Verify project setup and API key configuration"""

    print("="*60)
    print("Roast My CV - Setup Verification")
    print("="*60)

    issues = []
    warnings = []

    # Check 1: config.py exists
    print("\n1. Checking for config.py...")
    config_path = Path("config.py")
    if config_path.exists():
        print("   PASS: config.py found")

        # Check if API key is set
        try:
            from config import GEMINI_API_KEY

            if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
                print("   PASS: API key is configured")
                # Mask the key for security
                masked_key = GEMINI_API_KEY[:10] + "..." + GEMINI_API_KEY[-5:]
                print(f"   Key: {masked_key}")
            else:
                issues.append("API key not set in config.py")
                print("   FAIL: API key is not set (still shows YOUR_API_KEY_HERE)")
        except ImportError as e:
            issues.append(f"Cannot import from config.py: {e}")
            print(f"   FAIL: Cannot import config.py: {e}")
    else:
        issues.append("config.py not found")
        print("   FAIL: config.py not found")
        print("   Action: Run 'cp config.example.py config.py' and edit it")

    # Check 2: .gitignore protection
    print("\n2. Checking .gitignore protection...")
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()

        if "config.py" in gitignore_content:
            print("   PASS: config.py is protected in .gitignore")
        else:
            warnings.append(".gitignore doesn't protect config.py")
            print("   WARN: config.py not found in .gitignore")
    else:
        warnings.append(".gitignore not found")
        print("   WARN: .gitignore not found")

    # Check 3: Required directories
    print("\n3. Checking required directories...")
    required_dirs = ["data", "results", "notebooks"]
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"   PASS: {dir_name}/ exists")
        else:
            warnings.append(f"{dir_name}/ directory not found")
            print(f"   WARN: {dir_name}/ not found (will be created when needed)")

    # Check 4: Dependencies
    print("\n4. Checking Python dependencies...")
    missing_deps = []

    required_packages = [
        ("pandas", "Data handling"),
        ("google.generativeai", "Gemini API"),
        ("PyPDF2", "PDF processing"),
    ]

    for package, description in required_packages:
        try:
            __import__(package.replace(".", "_").replace("-", "_"))
            print(f"   PASS: {package} ({description})")
        except ImportError:
            missing_deps.append(package)
            print(f"   FAIL: {package} not installed ({description})")

    if missing_deps:
        issues.append(f"Missing dependencies: {', '.join(missing_deps)}")
        print("\n   Action: Run 'pip install -r requirements.txt'")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    if not issues and not warnings:
        print("\nPASS: All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("  - Run: jupyter notebook notebooks/06_quick_cv_roaster_v2.ipynb")
        print("  - Or: python process_new_cv.py your_cv.pdf")
        return 0
    else:
        if issues:
            print(f"\nFAIL: {len(issues)} critical issue(s) found:")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")

        if warnings:
            print(f"\nWARNINGS: {len(warnings)} warning(s):")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. {warning}")

        print("\nPlease fix the issues above before running the project.")
        return 1

if __name__ == "__main__":
    sys.exit(check_setup())

