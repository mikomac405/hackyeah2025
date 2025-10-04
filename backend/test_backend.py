#!/usr/bin/env python3
"""
Test script for Pension Simulator Backend
Run this after installing dependencies with: pip3 install -r requirements.txt
"""

import sys
import os

def test_imports():
    """Test if all imports work correctly"""
    try:
        print("Testing imports...")

        # Test Flask imports
        from flask import Flask
        print("✓ Flask imported successfully")

        # Test our app structure
        from app import create_app
        print("✓ App factory imported successfully")

        # Test API routes
        from routes.api import api_bp
        print("✓ API routes imported successfully")

        # Test pension calculator
        from models.pension_calculator import PensionCalculator
        print("✓ Pension calculator imported successfully")

        # Test report generator
        from utils.report_generator import generate_report
        print("✓ Report generator imported successfully")

        print("\n🎉 All imports successful! Backend structure is correct.")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies with: pip3 install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_app_creation():
    """Test if Flask app can be created"""
    try:
        print("\nTesting Flask app creation...")
        from app import create_app

        app = create_app()
        print("✓ Flask app created successfully")

        # Test if app has our routes
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        print(f"✓ App has {len(routes)} routes registered")

        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def test_pension_calculator():
    """Test pension calculator with sample data"""
    try:
        print("\nTesting pension calculator...")
        from models.pension_calculator import PensionCalculator

        calculator = PensionCalculator()

        # Sample input data
        sample_data = {
            'age': 35,
            'sex': 'M',
            'gross_salary': 5000,
            'work_start_year': 2010,
            'work_end_year': 2045
        }

        result = calculator.calculate_pension(sample_data)

        if 'error' not in result:
            print("✓ Pension calculation successful"            print(f"  - Actual amount: {result.get('actual_amount', 0)} PLN")
            print(f"  - Real amount: {result.get('real_amount', 0)} PLN")
            print(f"  - Replacement rate: {result.get('replacement_rate', 0)}%")
        else:
            print(f"❌ Calculation error: {result['error']}")

        return 'error' not in result

    except Exception as e:
        print(f"❌ Calculator test error: {e}")
        return False

if __name__ == "__main__":
    print("Pension Simulator Backend - Test Suite")
    print("=" * 50)

    success = True
    success &= test_imports()
    success &= test_app_creation()
    success &= test_pension_calculator()

    if success:
        print("\n✅ All tests passed! The backend is ready to run.")
        print("\nTo start the server:")
        print("  python3 app.py")
        print("\nAPI will be available at: http://localhost:5000")
        print("Health check: http://localhost:5000/health")
        print("Dashboard: http://localhost:5000/api/dashboard")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
