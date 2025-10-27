#!/usr/bin/env python3
"""
Test authentication function
"""

# Test that auth.py can be imported
try:
    from auth import require_authentication, is_admin
    print("✅ Authentication module imported successfully")
    print("✅ Admin password is: admin / iPSC_Lab2024!")
    print("✅ Ready to test - use 'streamlit run app.py'")
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")