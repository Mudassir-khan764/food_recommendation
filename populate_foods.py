#!/usr/bin/env python3
"""Simple script to populate MongoDB with food database"""

from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['meal_planner']
foods_collection = db['foods']

# Clear existing foods
foods_collection.delete_many({})

# Food database with nutrition data per 100g
foods = [
    # Breakfast items
    {'name': 'oatmeal', 'calories': 389, 'protein': 17, 'carbs': 66, 'fat': 7, 'portion_size': 50, 'portion_unit': 'g', 'category': 'breakfast'},
    {'name': 'eggs', 'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'portion_size': 1, 'portion_unit': 'piece', 'category': 'breakfast'},
    {'name': 'toast', 'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3.3, 'portion_size': 30, 'portion_unit': 'g', 'category': 'breakfast'},
    {'name': 'milk', 'calories': 61, 'protein': 3.2, 'carbs': 4.8, 'fat': 3.3, 'portion_size': 200, 'portion_unit': 'ml', 'category': 'breakfast'},
    {'name': 'yogurt', 'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'portion_size': 100, 'portion_unit': 'ml', 'category': 'breakfast'},
    {'name': 'banana', 'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'portion_size': 100, 'portion_unit': 'g', 'category': 'breakfast'},
    {'name': 'apple', 'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'portion_size': 100, 'portion_unit': 'g', 'category': 'breakfast'},
    {'name': 'orange', 'calories': 47, 'protein': 0.9, 'carbs': 12, 'fat': 0.1, 'portion_size': 100, 'portion_unit': 'g', 'category': 'breakfast'},
    {'name': 'honey', 'calories': 304, 'protein': 0.3, 'carbs': 82, 'fat': 0, 'portion_size': 1, 'portion_unit': 'piece', 'category': 'breakfast'},
    
    # Indian foods
    {'name': 'gulab_jamun', 'calories': 145, 'protein': 1.5, 'carbs': 28, 'fat': 3, 'portion_size': 1, 'portion_unit': 'piece', 'category': 'indian'},
    {'name': 'biryani', 'calories': 350, 'protein': 15, 'carbs': 45, 'fat': 12, 'portion_size': 250, 'portion_unit': 'g', 'category': 'indian'},
    {'name': 'samosa', 'calories': 262, 'protein': 5, 'carbs': 32, 'fat': 13, 'portion_size': 1, 'portion_unit': 'piece', 'category': 'indian'},
    {'name': 'dosa', 'calories': 133, 'protein': 2.5, 'carbs': 29, 'fat': 0.2, 'portion_size': 100, 'portion_unit': 'g', 'category': 'indian'},
    {'name': 'naan', 'calories': 262, 'protein': 8, 'carbs': 46, 'fat': 5, 'portion_size': 100, 'portion_unit': 'g', 'category': 'indian'},
    {'name': 'chapati', 'calories': 264, 'protein': 8, 'carbs': 43, 'fat': 7, 'portion_size': 100, 'portion_unit': 'g', 'category': 'indian'},
    {'name': 'dal', 'calories': 101, 'protein': 9, 'carbs': 18, 'fat': 0.5, 'portion_size': 150, 'portion_unit': 'g', 'category': 'indian'},
    {'name': 'curry', 'calories': 88, 'protein': 5, 'carbs': 12, 'fat': 1.5, 'portion_size': 150, 'portion_unit': 'g', 'category': 'indian'},
    
    # Vegetables
    {'name': 'spinach', 'calories': 23, 'protein': 2.7, 'carbs': 3.6, 'fat': 0.4, 'portion_size': 100, 'portion_unit': 'g', 'category': 'vegetables'},
    {'name': 'broccoli', 'calories': 34, 'protein': 2.8, 'carbs': 7, 'fat': 0.4, 'portion_size': 100, 'portion_unit': 'g', 'category': 'vegetables'},
    {'name': 'carrot', 'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2, 'portion_size': 100, 'portion_unit': 'g', 'category': 'vegetables'},
    {'name': 'tomato', 'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'portion_size': 100, 'portion_unit': 'g', 'category': 'vegetables'},
    {'name': 'cucumber', 'calories': 16, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'portion_size': 100, 'portion_unit': 'g', 'category': 'vegetables'},
    {'name': 'lettuce', 'calories': 15, 'protein': 1.4, 'carbs': 2.9, 'fat': 0.2, 'portion_size': 100, 'portion_unit': 'g', 'category': 'vegetables'},
    
    # Main dishes
    {'name': 'pizza', 'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10, 'portion_size': 100, 'portion_unit': 'g', 'category': 'main'},
    {'name': 'burger', 'calories': 354, 'protein': 15, 'carbs': 35, 'fat': 16, 'portion_size': 215, 'portion_unit': 'g', 'category': 'main'},
    {'name': 'sandwich', 'calories': 265, 'protein': 9, 'carbs': 35, 'fat': 9, 'portion_size': 100, 'portion_unit': 'g', 'category': 'main'},
    {'name': 'pasta', 'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1, 'portion_size': 100, 'portion_unit': 'g', 'category': 'main'},
    {'name': 'rice', 'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'portion_size': 100, 'portion_unit': 'g', 'category': 'main'},
    {'name': 'chicken', 'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'portion_size': 100, 'portion_unit': 'g', 'category': 'main'},
    {'name': 'fish', 'calories': 96, 'protein': 20, 'carbs': 0, 'fat': 1, 'portion_size': 100, 'portion_unit': 'g', 'category': 'main'},
    {'name': 'beef', 'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 17, 'portion_size': 100, 'portion_unit': 'g', 'category': 'main'},
    
    # Snacks
    {'name': 'almonds', 'calories': 579, 'protein': 21, 'carbs': 22, 'fat': 50, 'portion_size': 28, 'portion_unit': 'g', 'category': 'snacks'},
    {'name': 'peanuts', 'calories': 567, 'protein': 26, 'carbs': 16, 'fat': 49, 'portion_size': 28, 'portion_unit': 'g', 'category': 'snacks'},
    {'name': 'peanut_butter', 'calories': 588, 'protein': 25, 'carbs': 20, 'fat': 50, 'portion_size': 32, 'portion_unit': 'g', 'category': 'snacks'},
    {'name': 'cheese', 'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33, 'portion_size': 30, 'portion_unit': 'g', 'category': 'snacks'},
    {'name': 'ice_cream', 'calories': 207, 'protein': 3.5, 'carbs': 24, 'fat': 11, 'portion_size': 100, 'portion_unit': 'ml', 'category': 'snacks'},
    {'name': 'donut', 'calories': 452, 'protein': 4.6, 'carbs': 51, 'fat': 25, 'portion_size': 50, 'portion_unit': 'g', 'category': 'snacks'},
    {'name': 'chocolate', 'calories': 546, 'protein': 4.9, 'carbs': 61, 'fat': 31, 'portion_size': 30, 'portion_unit': 'g', 'category': 'snacks'},
    {'name': 'protein_bar', 'calories': 210, 'protein': 20, 'carbs': 21, 'fat': 6, 'portion_size': 50, 'portion_unit': 'g', 'category': 'snacks'},
    {'name': 'granola', 'calories': 471, 'protein': 13, 'carbs': 64, 'fat': 20, 'portion_size': 50, 'portion_unit': 'g', 'category': 'snacks'},
]

# Insert foods into MongoDB
result = foods_collection.insert_many(foods)
print(f"✅ Successfully inserted {len(result.inserted_ids)} foods into database")
print(f"Total foods in database: {foods_collection.count_documents({})}")

# Verify insertion
categories = foods_collection.distinct('category')
print(f"Categories: {', '.join(categories)}")
