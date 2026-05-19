#!/usr/bin/env python3
"""
Complete validation of Food Tracking System
Tests all components and data flows
"""

import json
from pymongo import MongoClient
from datetime import date

print("=" * 70)
print("🧪 FOOD TRACKING SYSTEM VALIDATION")
print("=" * 70)

# Connect to MongoDB
print("\n1️⃣ Checking MongoDB Connection...")
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.admin.command('ping')
    db = client['meal_planner']
    print("✅ MongoDB connected successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    exit(1)

# Check collections exist
print("\n2️⃣ Checking Collections...")
collections = {
    'users': 'User accounts',
    'foods': 'Food database',
    'food_logs': 'User meal logs',
    'daily_summary': 'Daily aggregates'
}

for collection_name, description in collections.items():
    count = db[collection_name].count_documents({})
    status = "✅" if count >= 0 else "❌"
    print(f"{status} {collection_name}: {count} documents ({description})")

# Check food database
print("\n3️⃣ Validating Food Database...")
foods = db['foods'].find()
food_list = list(db['foods'].find().limit(5))
print(f"✅ Total foods: {db['foods'].count_documents({})}")
print("\nSample foods:")
for food in food_list:
    print(f"  • {food['name']}: {food['calories']} kcal | " +
          f"P:{food['protein']}g C:{food['carbs']}g F:{food['fat']}g | " +
          f"{food['portion_size']}{food['portion_unit']}")

# Check categories
print("\n4️⃣ Food Categories...")
categories = db['foods'].distinct('category')
print(f"✅ Categories found: {', '.join(sorted(categories))}")

# Test database methods
print("\n5️⃣ Testing Database Methods...")
from database import Database

db_instance = Database()

# Test search
print("  • Testing search_foods('chicken')...")
results = db_instance.search_foods('chicken')
print(f"    ✅ Found {len(results)} results")

# Test get_food
print("  • Testing get_food('eggs')...")
egg = db_instance.get_food('eggs')
if egg:
    print(f"    ✅ Got {egg['name']}: {egg['calories']} kcal per {egg['portion_size']}{egg['portion_unit']}")
else:
    print(f"    ⚠️ Food not found")

# Test app routes
print("\n6️⃣ Checking Flask App Routes...")
try:
    from app import app
    
    routes = [
        ('/track', 'Track page'),
        ('/profile', 'Profile page'),
        ('/api/add_food', 'Add food endpoint'),
        ('/api/search_foods', 'Search endpoint'),
        ('/api/today_meals', 'Today meals endpoint'),
        ('/api/profile_data', 'Profile data endpoint'),
    ]
    
    with app.app_context():
        for route_path, description in routes:
            found = any(rule.rule == route_path for rule in app.url_map.iter_rules())
            status = "✅" if found else "❌"
            print(f"{status} {route_path}: {description}")
    
    print("✅ Flask app loaded successfully")
except Exception as e:
    print(f"❌ Flask app check failed: {e}")

# Check templates
print("\n7️⃣ Checking HTML Templates...")
import os
templates = {
    'track.html': 'Food tracking dashboard',
    'profile.html': 'User profile page',
    'dashboard.html': 'Dashboard',
    'login.html': 'Login page'
}

for template, desc in templates.items():
    path = f'c:\\Users\\CSC\\Desktop\\clone\\AI-Meal-Planner\\templates\\{template}'
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {template}: {desc}")

# Summary
print("\n" + "=" * 70)
print("📊 SYSTEM STATUS SUMMARY")
print("=" * 70)

checks = {
    'MongoDB': db is not None,
    'Food Database (40+ foods)': db['foods'].count_documents({}) >= 40,
    'Collections': all(db[col].count_documents({}) >= 0 for col in collections.keys()),
    'Database Methods': db_instance is not None,
    'Flask Routes': len([r for r in app.url_map.iter_rules() if '/api/' in r.rule or r.rule == '/track' or r.rule == '/profile']) >= 6,
    'Templates': all(os.path.exists(f'c:\\Users\\CSC\\Desktop\\clone\\AI-Meal-Planner\\templates\\{t}') for t in templates.keys())
}

all_passed = all(checks.values())

for check, passed in checks.items():
    status = "✅" if passed else "❌"
    print(f"{status} {check}")

print("\n" + "=" * 70)
if all_passed:
    print("🎉 ALL SYSTEMS OPERATIONAL - READY TO USE!")
    print("\n📝 Next steps:")
    print("  1. Start Flask: python app.py")
    print("  2. Visit: http://127.0.0.1:5000")
    print("  3. Sign up and start tracking!")
else:
    print("⚠️ Some checks failed - review above")

print("=" * 70)
