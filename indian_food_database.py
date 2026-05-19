import json
import os

# Indian Food Database with nutritional information and prices (per 100g)
INDIAN_FOOD_DATABASE = {
    # Cereals & Grains
    "rice": {
        "calories": 130,
        "protein": 2.7,
        "iron": 0.2,
        "vitamin_b12": 0,
        "carbs": 28,
        "fat": 0.3,
        "price_per_100g": 2.5,  # ₹2.50 per 100g
        "category": "cereal",
        "veg": True
    },
    "wheat_flour": {
        "calories": 361,
        "protein": 12.6,
        "iron": 3.6,
        "vitamin_b12": 0,
        "carbs": 76,
        "fat": 1.5,
        "price_per_100g": 3.0,
        "category": "cereal",
        "veg": True
    },
    "oats": {
        "calories": 379,
        "protein": 13.2,
        "iron": 4.7,
        "vitamin_b12": 0,
        "carbs": 66,
        "fat": 6.9,
        "price_per_100g": 8.0,
        "category": "cereal",
        "veg": True
    },
    "poha": {
        "calories": 350,
        "protein": 7.0,
        "iron": 1.2,
        "vitamin_b12": 0,
        "carbs": 77,
        "fat": 0.5,
        "price_per_100g": 4.0,
        "category": "cereal",
        "veg": True
    },

    # Pulses & Lentils
    "moong_dal": {
        "calories": 347,
        "protein": 24.0,
        "iron": 6.7,
        "vitamin_b12": 0,
        "carbs": 63,
        "fat": 1.2,
        "price_per_100g": 8.0,
        "category": "pulse",
        "veg": True
    },
    "chana_dal": {
        "calories": 378,
        "protein": 20.0,
        "iron": 4.7,
        "vitamin_b12": 0,
        "carbs": 67,
        "fat": 6.0,
        "price_per_100g": 7.0,
        "category": "pulse",
        "veg": True
    },
    "urad_dal": {
        "calories": 341,
        "protein": 25.0,
        "iron": 7.6,
        "vitamin_b12": 0,
        "carbs": 59,
        "fat": 1.4,
        "price_per_100g": 9.0,
        "category": "pulse",
        "veg": True
    },
    "chickpeas": {
        "calories": 364,
        "protein": 19.0,
        "iron": 6.2,
        "vitamin_b12": 0,
        "carbs": 61,
        "fat": 6.0,
        "price_per_100g": 6.0,
        "category": "pulse",
        "veg": True
    },
    "soy_chunks": {
        "calories": 345,
        "protein": 52.0,
        "iron": 10.4,
        "vitamin_b12": 0,
        "carbs": 33,
        "fat": 1.0,
        "price_per_100g": 12.0,
        "category": "pulse",
        "veg": True
    },

    # Dairy
    "milk": {
        "calories": 61,
        "protein": 3.2,
        "iron": 0.1,
        "vitamin_b12": 0.4,
        "carbs": 4.8,
        "fat": 3.3,
        "price_per_100g": 3.5,
        "category": "dairy",
        "veg": True
    },
    "curd": {
        "calories": 61,
        "protein": 3.4,
        "iron": 0.1,
        "vitamin_b12": 0.4,
        "carbs": 4.7,
        "fat": 3.3,
        "price_per_100g": 4.0,
        "category": "dairy",
        "veg": True
    },
    "paneer": {
        "calories": 265,
        "protein": 18.3,
        "iron": 0.7,
        "vitamin_b12": 0.4,
        "carbs": 3.6,
        "fat": 20.8,
        "price_per_100g": 25.0,
        "category": "dairy",
        "veg": True
    },

    # Eggs & Meat (Non-Veg)
    "eggs": {
        "calories": 155,
        "protein": 13.0,
        "iron": 1.8,
        "vitamin_b12": 0.9,
        "carbs": 1.1,
        "fat": 11.0,
        "price_per_100g": 6.0,  # ~₹6 per egg (50g each)
        "category": "protein",
        "veg": False
    },
    "chicken": {
        "calories": 165,
        "protein": 31.0,
        "iron": 1.3,
        "vitamin_b12": 0.3,
        "carbs": 0,
        "fat": 3.6,
        "price_per_100g": 15.0,
        "category": "protein",
        "veg": False
    },
    "fish": {
        "calories": 206,
        "protein": 22.0,
        "iron": 0.9,
        "vitamin_b12": 2.4,
        "carbs": 0,
        "fat": 12.0,
        "price_per_100g": 20.0,
        "category": "protein",
        "veg": False
    },

    # Vegetables
    "potatoes": {
        "calories": 77,
        "protein": 2.0,
        "iron": 0.8,
        "vitamin_b12": 0,
        "carbs": 17,
        "fat": 0.1,
        "price_per_100g": 2.0,
        "category": "vegetable",
        "veg": True
    },
    "onions": {
        "calories": 40,
        "protein": 1.1,
        "iron": 0.2,
        "vitamin_b12": 0,
        "carbs": 9.3,
        "fat": 0.1,
        "price_per_100g": 3.0,
        "category": "vegetable",
        "veg": True
    },
    "tomatoes": {
        "calories": 18,
        "protein": 0.9,
        "iron": 0.3,
        "vitamin_b12": 0,
        "carbs": 3.9,
        "fat": 0.2,
        "price_per_100g": 4.0,
        "category": "vegetable",
        "veg": True
    },
    "spinach": {
        "calories": 23,
        "protein": 2.9,
        "iron": 2.7,
        "vitamin_b12": 0,
        "carbs": 3.6,
        "fat": 0.4,
        "price_per_100g": 5.0,
        "category": "vegetable",
        "veg": True
    },
    "carrots": {
        "calories": 41,
        "protein": 0.9,
        "iron": 0.3,
        "vitamin_b12": 0,
        "carbs": 9.6,
        "fat": 0.2,
        "price_per_100g": 3.5,
        "category": "vegetable",
        "veg": True
    },
    "cabbage": {
        "calories": 25,
        "protein": 1.3,
        "iron": 0.5,
        "vitamin_b12": 0,
        "carbs": 5.8,
        "fat": 0.1,
        "price_per_100g": 2.5,
        "category": "vegetable",
        "veg": True
    },

    # Fruits
    "bananas": {
        "calories": 89,
        "protein": 1.1,
        "iron": 0.3,
        "vitamin_b12": 0,
        "carbs": 23,
        "fat": 0.3,
        "price_per_100g": 4.0,
        "category": "fruit",
        "veg": True
    },
    "apples": {
        "calories": 52,
        "protein": 0.3,
        "iron": 0.1,
        "vitamin_b12": 0,
        "carbs": 14,
        "fat": 0.2,
        "price_per_100g": 8.0,
        "category": "fruit",
        "veg": True
    },
    "oranges": {
        "calories": 47,
        "protein": 0.9,
        "iron": 0.1,
        "vitamin_b12": 0,
        "carbs": 12,
        "fat": 0.1,
        "price_per_100g": 6.0,
        "category": "fruit",
        "veg": True
    },

    # Nuts & Seeds
    "peanuts": {
        "calories": 567,
        "protein": 25.8,
        "iron": 4.6,
        "vitamin_b12": 0,
        "carbs": 16,
        "fat": 49.2,
        "price_per_100g": 15.0,
        "category": "nut",
        "veg": True
    },
    "almonds": {
        "calories": 579,
        "protein": 21.2,
        "iron": 3.7,
        "vitamin_b12": 0,
        "carbs": 22,
        "fat": 49.9,
        "price_per_100g": 40.0,
        "category": "nut",
        "veg": True
    },

    # Oils & Fats
    "ghee": {
        "calories": 900,
        "protein": 0,
        "iron": 0,
        "vitamin_b12": 0,
        "carbs": 0,
        "fat": 100,
        "price_per_100g": 35.0,
        "category": "fat",
        "veg": True
    },
    "mustard_oil": {
        "calories": 884,
        "protein": 0,
        "iron": 0,
        "vitamin_b12": 0,
        "carbs": 0,
        "fat": 100,
        "price_per_100g": 18.0,
        "category": "fat",
        "veg": True
    },

    # Spices & Condiments
    "turmeric": {
        "calories": 312,
        "protein": 9.7,
        "iron": 55.0,
        "vitamin_b12": 0,
        "carbs": 67.1,
        "fat": 3.3,
        "price_per_100g": 20.0,
        "category": "spice",
        "veg": True
    },
    "cumin": {
        "calories": 375,
        "protein": 17.8,
        "iron": 66.4,
        "vitamin_b12": 0,
        "carbs": 44.2,
        "fat": 22.3,
        "price_per_100g": 25.0,
        "category": "spice",
        "veg": True
    }
}

# Minimum recommended daily intake for deficiencies
NUTRIENT_REQUIREMENTS = {
    "iron": 14,  # mg per day for women
    "vitamin_b12": 2.4,  # mcg per day
    "protein": None,  # Calculated based on weight and goal
    "calories": None  # User specified
}

def save_food_database():
    """Save the food database to a JSON file"""
    with open('indian_food_database.json', 'w') as f:
        json.dump(INDIAN_FOOD_DATABASE, f, indent=2)

if __name__ == "__main__":
    save_food_database()
    print("Food database saved to indian_food_database.json")