#!/usr/bin/env python3
"""
Test script for the AI Nutrition Optimization Engine
"""

import requests
import json

def test_nutrition_optimizer():
    """Test the nutrition optimizer endpoint"""

    # Test data
    test_data = {
        "daily_calories": 2000,
        "weekly_budget": 1000,
        "goal": "weight loss",
        "weight": 70,
        "deficiencies": ["iron"],
        "diet_preference": "veg"
    }

    try:
        # Make request to the endpoint
        response = requests.post(
            'http://localhost:5000/optimize-nutrition',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Nutrition optimizer test successful!")
            print("\n📋 Grocery Plan Summary:")
            print(f"Total Cost: ₹{result['plan']['total_cost']:.1f}")
            print(f"Budget Remaining: ₹{result['plan']['budget_remaining']:.1f}")
            print(f"Calories: {result['plan']['total_calories']:.0f}/14000")
            print(f"Protein: {result['plan']['total_protein']:.1f}g")
            print(f"Deficiencies Fixed: {result['plan']['deficiencies_fixed']}")
            print(f"Efficiency Score: {result['plan']['nutrition_efficiency_score']:.1f}/100")

            print("\n🛒 Grocery List:")
            for food, quantity in result['plan']['groceries'].items():
                food_data = result['plan']['groceries']  # This should be from the database
                print(f"• {food.replace('_', ' ').title()}: {quantity}g")

        else:
            print(f"❌ Test failed with status code: {response.status_code}")
            print(f"Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server. Make sure the app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_nutrition_optimizer()