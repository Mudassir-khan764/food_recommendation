"""
Initialize Food Database with Common Foods and Their Nutrition Info
Calories, Protein, Carbs, Fat per standard portion
"""

from database import Database

def init_food_database():
    """Populate MongoDB with common foods"""
    db = Database()
    
    # Common foods with nutrition data (per 100g standard)
    foods = [
        # Breakfast Foods
        {'name': 'oatmeal', 'calories': 150, 'protein': 5, 'carbs': 27, 'fat': 3, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'eggs', 'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'toast_brown', 'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'milk_full_fat', 'calories': 61, 'protein': 3.2, 'carbs': 4.8, 'fat': 3.3, 'portion_size': 100, 'portion_unit': 'ml'},
        {'name': 'yogurt_plain', 'calories': 59, 'protein': 3.5, 'carbs': 3.3, 'fat': 0.4, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'banana', 'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'apple', 'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'orange', 'calories': 47, 'protein': 0.9, 'carbs': 12, 'fat': 0.1, 'portion_size': 100, 'portion_unit': 'g'},
        
        # Indian Foods
        {'name': 'gulab_jamun', 'calories': 145, 'protein': 1.2, 'carbs': 20, 'fat': 6, 'portion_size': 20, 'portion_unit': 'piece'},
        {'name': 'biryani', 'calories': 195, 'protein': 6, 'carbs': 30, 'fat': 5, 'portion_size': 150, 'portion_unit': 'g'},
        {'name': 'samosa', 'calories': 266, 'protein': 5, 'carbs': 30, 'fat': 14, 'portion_size': 50, 'portion_unit': 'piece'},
        {'name': 'dosa', 'calories': 168, 'protein': 5, 'carbs': 22, 'fat': 6, 'portion_size': 150, 'portion_unit': 'g'},
        {'name': 'naan', 'calories': 262, 'protein': 9, 'carbs': 43, 'fat': 5, 'portion_size': 80, 'portion_unit': 'g'},
        {'name': 'chapati', 'calories': 165, 'protein': 5.5, 'carbs': 32, 'fat': 1.3, 'portion_size': 50, 'portion_unit': 'g'},
        {'name': 'dal', 'calories': 85, 'protein': 3, 'carbs': 15, 'fat': 0.5, 'portion_size': 150, 'portion_unit': 'g'},
        {'name': 'curry', 'calories': 165, 'protein': 8, 'carbs': 12, 'fat': 8, 'portion_size': 150, 'portion_unit': 'g'},
        
        # Vegetables
        {'name': 'spinach', 'calories': 23, 'protein': 2.7, 'carbs': 3.6, 'fat': 0.4, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'broccoli', 'calories': 34, 'protein': 2.8, 'carbs': 7, 'fat': 0.4, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'carrot', 'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'tomato', 'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'cucumber', 'calories': 16, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'portion_size': 100, 'portion_unit': 'g'},
        
        # Main Dishes
        {'name': 'pizza', 'calories': 266, 'protein': 12, 'carbs': 36, 'fat': 10, 'portion_size': 100, 'portion_unit': 'slice'},
        {'name': 'burger', 'calories': 540, 'protein': 28, 'carbs': 41, 'fat': 28, 'portion_size': 100, 'portion_unit': 'piece'},
        {'name': 'sandwich', 'calories': 320, 'protein': 12, 'carbs': 45, 'fat': 10, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'pasta', 'calories': 220, 'protein': 8, 'carbs': 43, 'fat': 1, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'rice', 'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'chicken_breast', 'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'fish', 'calories': 206, 'protein': 22, 'carbs': 0, 'fat': 12, 'portion_size': 100, 'portion_unit': 'g'},
        
        # Snacks & Others
        {'name': 'almonds', 'calories': 579, 'protein': 21, 'carbs': 22, 'fat': 50, 'portion_size': 28, 'portion_unit': 'g'},
        {'name': 'peanut_butter', 'calories': 588, 'protein': 25, 'carbs': 20, 'fat': 50, 'portion_size': 32, 'portion_unit': 'g'},
        {'name': 'cheese', 'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33, 'portion_size': 28, 'portion_unit': 'g'},
        {'name': 'ice_cream', 'calories': 207, 'protein': 3.5, 'carbs': 24, 'fat': 11, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'donut', 'calories': 452, 'protein': 4.6, 'carbs': 51, 'fat': 25, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'chocolate', 'calories': 546, 'protein': 5, 'carbs': 57, 'fat': 32, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'nuts_mixed', 'calories': 655, 'protein': 20, 'carbs': 27, 'fat': 59, 'portion_size': 100, 'portion_unit': 'g'},
        {'name': 'protein_bar', 'calories': 200, 'protein': 20, 'carbs': 15, 'fat': 7, 'portion_size': 50, 'portion_unit': 'g'},
    ]
    
    # Insert foods into database
    count = 0
    for food in foods:
        try:
            db.add_food(
                food_name=food['name'],
                calories=food['calories'],
                protein=food['protein'],
                carbs=food['carbs'],
                fat=food['fat'],
                portion_size=food['portion_size'],
                portion_unit=food['portion_unit']
            )
            count += 1
            print(f"✓ Added: {food['name']}")
        except Exception as e:
            print(f"✗ Failed to add {food['name']}: {e}")
    
    print(f"\n✓ Successfully initialized {count} foods in database!")

if __name__ == '__main__':
    init_food_database()
