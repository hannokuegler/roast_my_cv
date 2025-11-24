#!/usr/bin/env python3
"""
Quick test to verify Gemini API works with correct model name
"""

import sys

print("Testing Gemini API connection...")
print("="*60)

# Test 1: Import config
print("\n1. Loading API key from config.py...")
try:
    from config import GEMINI_API_KEY
    masked_key = GEMINI_API_KEY[:10] + "..." + GEMINI_API_KEY[-5:]
    print(f"   PASS: API key loaded ({masked_key})")
except Exception as e:
    print(f"   FAIL: {e}")
    sys.exit(1)

# Test 2: Import Gemini library
print("\n2. Importing google.generativeai...")
try:
    import google.generativeai as genai
    print("   PASS: Library imported")
except ImportError as e:
    print("   FAIL: Library not installed")
    print("   Run: pip install google-generativeai")
    sys.exit(1)

# Test 3: Configure API
print("\n3. Configuring API...")
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("   PASS: API configured")
except Exception as e:
    print(f"   FAIL: {e}")
    sys.exit(1)

# Test 4: List available models
print("\n4. Listing available models...")
try:
    models = genai.list_models()
    flash_models = [m.name for m in models if 'flash' in m.name.lower()]
    print("   Available Flash models:")
    for model in flash_models[:5]:
        print(f"     - {model}")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 5: Test model with simple request
print("\n5. Testing model with simple request...")
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say 'API test successful' in 3 words")
    print(f"   PASS: Model responded")
    print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"   FAIL: {e}")
    print("\n   Available models:")
    print("     - gemini-2.5-flash (newest)")
    print("     - gemini-2.0-flash (experimental)")
    print("     - gemini-2.0-flash")
    sys.exit(1)

print("\n" + "="*60)
print("SUCCESS: API is working correctly!")
print("="*60)
print("\nYou can now run the notebooks:")
print("  jupyter notebook notebooks/06_quick_cv_roaster_v2.ipynb")
