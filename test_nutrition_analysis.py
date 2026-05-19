#!/usr/bin/env python3
"""
Test script for Nutrition Analysis API
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_nutrition_analysis():
    """Test the nutrition analysis API with authentication"""

    # Create a session to maintain cookies
    session = requests.Session()

    print("Testing Nutrition Analysis API...")

    try:
        # First, try to login (you'll need to replace with actual credentials)
        login_data = {
            'email': 'test@example.com',  # Replace with actual test user
            'password': 'password123'     # Replace with actual password
        }

        print("Attempting login...")
        login_response = session.post(f'{BASE_URL}/login', json=login_data)
        print(f"Login response: {login_response.status_code}")

        if login_response.status_code == 200:
            login_result = login_response.json()
            if login_result.get('success'):
                print("✓ Login successful")

                # Now test nutrition analysis
                analysis_data = {
                    'calories': 2200,
                    'protein': 120,
                    'carbs': 250,
                    'fats': 80,
                    'sugar': 50,
                    'fiber': 25,
                    'sodium': 2000,
                    'water': 1800,
                    'meals': ['breakfast', 'lunch', 'dinner']
                }

                print("Testing nutrition analysis...")
                analysis_response = session.post(f'{BASE_URL}/api/analyze-nutrition',
                                               json=analysis_data)
                print(f"Analysis response: {analysis_response.status_code}")

                if analysis_response.status_code == 200:
                    result = analysis_response.json()
                    if result.get('success'):
                        print("✓ Nutrition analysis successful!")
                        print(f"Insights received: {len(result.get('insights', []))}")
                        for i, insight in enumerate(result.get('insights', []), 1):
                            print(f"  {i}. {insight}")
                    else:
                        print(f"✗ Analysis failed: {result.get('error')}")
                else:
                    print(f"✗ Analysis request failed: {analysis_response.status_code}")
                    print(f"Response: {analysis_response.text}")

            else:
                print(f"✗ Login failed: {login_result.get('error')}")
        else:
            print(f"✗ Login request failed: {login_response.status_code}")
            print("Note: You may need to create a test user first or use existing credentials")

    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to Flask app. Make sure it's running on port 5000.")
    except Exception as e:
        print(f"✗ Test failed: {e}")

if __name__ == '__main__':
    test_nutrition_analysis()