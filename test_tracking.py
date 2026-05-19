#!/usr/bin/env python3
"""Test food tracking system"""

import requests
import json
from pymongo import MongoClient

# Base URL
BASE_URL = 'http://127.0.0.1:5000'

# Create a session
session = requests.Session()

# Test credentials
test_email = 'testuser@example.com'
test_password = 'test12345'
test_name = 'Test User'

print("🧪 Testing Food Tracking System")
print("=" * 50)

# 1. Signup
print("\n1️⃣ Signup Test")
signup_data = {
    'email': test_email,
    'first_name': test_name.split()[0],
    'last_name': test_name.split()[1],
    'password': test_password,
    'confirm_password': test_password
}
response = session.post(f'{BASE_URL}/signup', data=signup_data, allow_redirects=False)
print(f"Status: {response.status_code}")
if response.status_code in [302, 200]:  # Redirect or success
    print("✅ Signup successful")
else:
    print(f"❌ Signup failed: {response.text[:200]}")

# 2. Login
print("\n2️⃣ Login Test")
login_data = {
    'email': test_email,
    'password': test_password
}
response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
print(f"Status: {response.status_code}")
if response.status_code in [302, 200]:
    print("✅ Login successful")
else:
    print(f"❌ Login failed: {response.text[:200]}")

# 3. Get food list
print("\n3️⃣ Search Foods Test")
response = session.get(f'{BASE_URL}/api/search_foods?q=chicken')
print(f"Status: {response.status_code}")
foods = response.json() if response.status_code == 200 else []
print(f"Found {len(foods)} foods matching 'chicken'")
if foods:
    print(f"  Sample: {foods[0]['name']} - {foods[0]['calories']} kcal per {foods[0]['portion_size']}{foods[0]['portion_unit']}")
    print("✅ Search foods successful")
else:
    print("❌ No foods found")

# 4. Add food to meal
print("\n4️⃣ Add Food Test")
add_data = {
    'meal_type': 'breakfast',
    'food_name': 'eggs',
    'quantity': 200,
    'portion_type': 'g'
}
response = session.post(f'{BASE_URL}/api/add_food', json=add_data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    if result.get('success'):
        print(f"✅ Food added successfully")
        meals = result.get('today_meals', {})
        breakfast = meals.get('breakfast', [])
        print(f"   Breakfast items: {len(breakfast)}")
        summary = result.get('today_summary', {})
        print(f"   Total calories: {summary.get('calories', 0)}")
    else:
        print(f"❌ Add food failed: {result.get('error')}")
else:
    print(f"❌ Add food error: {response.text[:200]}")

# 5. Get today's meals
print("\n5️⃣ Get Today's Meals Test")
response = session.get(f'{BASE_URL}/api/today_meals')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    if result.get('success'):
        meals = result.get('meals', {})
        summary = result.get('summary', {})
        print("✅ Today's meals retrieved successfully")
        for meal_type, foods in meals.items():
            if foods:
                print(f"   {meal_type.upper()}: {len(foods)} items")
        print(f"   Total: {summary.get('calories', 0)} kcal | P:{summary.get('protein', 0)}g | C:{summary.get('carbs', 0)}g | F:{summary.get('fat', 0)}g")
    else:
        print(f"❌ Error: {result.get('error')}")
else:
    print(f"❌ Request error: {response.text[:200]}")

# 6. Get profile data
print("\n6️⃣ Get Profile Data Test")
response = session.get(f'{BASE_URL}/api/profile_data')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    if result.get('success'):
        print("✅ Profile data retrieved successfully")
        print(f"   Email: {result.get('email')}")
        goals = result.get('daily_goals', {})
        print(f"   Goals: {goals.get('daily_calorie_goal')} kcal | P:{goals.get('daily_protein_goal')}g")
    else:
        print(f"❌ Error: {result.get('error')}")
else:
    print(f"❌ Request error: {response.text[:200]}")

# 7. Add another food and test remove
print("\n7️⃣ Add Another Food Test")
add_data = {
    'meal_type': 'lunch',
    'food_name': 'chicken',
    'quantity': 150,
    'portion_type': 'g'
}
response = session.post(f'{BASE_URL}/api/add_food', json=add_data)
if response.status_code == 200:
    result = response.json()
    if result.get('success'):
        food_log_id = result.get('food_log_id')
        print(f"✅ Food added successfully (ID: {food_log_id})")
        
        # 8. Remove food
        print("\n8️⃣ Remove Food Test")
        response = session.delete(f'{BASE_URL}/api/remove_food/{food_log_id}')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Food removed successfully")
            else:
                print(f"❌ Remove failed: {result.get('error')}")
        else:
            print(f"❌ Remove error: {response.text[:200]}")
    else:
        print(f"❌ Add food failed: {result.get('error')}")

print("\n" + "=" * 50)
print("🎉 Test Complete!")
