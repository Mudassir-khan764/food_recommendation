import random
from data import food_items_breakfast, food_items_lunch, food_items_dinner

def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        bmr = 9.99 * weight + 6.25 * height - 4.92 * age + 5
    else:
        bmr = 9.99 * weight + 6.25 * height - 4.92 * age - 161
    return bmr

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extremely Active": 1.9
    }
    return bmr * activity_multipliers[activity_level]

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return bmi

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_water_intake(weight, activity_level):
    base_water = weight * 35
    if activity_level in ["Very Active", "Extremely Active"]:
        base_water += 500
    elif activity_level in ["Moderately Active"]:
        base_water += 250
    return base_water / 1000

def adjust_calories_for_goal(tdee, goal):
    if goal == "Weight Loss":
        return tdee - 500
    elif goal == "Weight Gain":
        return tdee + 500
    elif goal == "Muscle Gain":
        return tdee + 300
    else:
        return tdee

def filter_foods_by_preferences(food_dict, diet_type, allergies):
    filtered_dict = {}
    
    for category, foods in food_dict.items():
        filtered_foods = {}
        for food, calories in foods.items():
            if diet_type == "Vegetarian":
                non_veg_items = ["chicken", "beef", "salmon", "shrimp", "turkey", "smoked_salmon", "mutton", "fish"]
                if any(item in food.lower() for item in non_veg_items):
                    continue
            elif diet_type == "Vegan":
                non_vegan_items = ["chicken", "beef", "salmon", "shrimp", "turkey", "smoked_salmon", 
                                 "eggs", "milk", "cheese", "yogurt", "cottage_cheese", "greek_yogurt", 
                                 "paneer", "ghee", "mutton", "fish", "curd", "lassi"]
                if any(item in food.lower() for item in non_vegan_items):
                    continue
            
            skip_food = False
            for allergy in allergies:
                if allergy == "Nuts" and (("nut" in food.lower()) or ("almond" in food.lower()) or ("walnut" in food.lower())):
                    skip_food = True
                elif allergy == "Dairy" and any(dairy in food.lower() for dairy in ["milk", "cheese", "yogurt", "paneer", "ghee", "curd"]):
                    skip_food = True
                elif allergy == "Gluten" and any(gluten in food.lower() for gluten in ["wheat", "bread", "pasta", "cereal", "naan", "roti"]):
                    skip_food = True
                elif allergy == "Eggs" and "egg" in food.lower():
                    skip_food = True
            
            if not skip_food:
                filtered_foods[food] = calories
        
        if filtered_foods:
            filtered_dict[category] = filtered_foods
    
    return filtered_dict

def knapsack(target_calories, food_groups):
    items = []
    for group, foods in food_groups.items():
        for item, calories in foods.items():
            items.append((calories, item))

    n = len(items)
    if n == 0:
        return [], 0
        
    dp = [[0 for _ in range(target_calories + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(target_calories + 1):
            value, _ = items[i - 1]

            if value > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - value] + value)

    selected_items = []
    j = target_calories
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            _, item = items[i - 1]
            selected_items.append(item)
            j -= items[i - 1][0]

    return selected_items, dp[n][target_calories]

def generate_meal_plan(target_calories, diet_type, allergies):
    filtered_breakfast = filter_foods_by_preferences(food_items_breakfast, diet_type, allergies)
    filtered_lunch = filter_foods_by_preferences(food_items_lunch, diet_type, allergies)
    filtered_dinner = filter_foods_by_preferences(food_items_dinner, diet_type, allergies)
    
    if not filtered_breakfast or not filtered_lunch or not filtered_dinner:
        return None
    
    calories_breakfast = int(target_calories * 0.3)
    calories_lunch = int(target_calories * 0.4)
    calories_dinner = int(target_calories * 0.3)
    
    breakfast_items, cal_b = knapsack(calories_breakfast, filtered_breakfast)
    lunch_items, cal_l = knapsack(calories_lunch, filtered_lunch)
    dinner_items, cal_d = knapsack(calories_dinner, filtered_dinner)
    
    return {
        'breakfast': {
            'items': [item.replace('_', ' ').title() for item in breakfast_items],
            'calories': cal_b,
            'target': calories_breakfast
        },
        'lunch': {
            'items': [item.replace('_', ' ').title() for item in lunch_items],
            'calories': cal_l,
            'target': calories_lunch
        },
        'dinner': {
            'items': [item.replace('_', ' ').title() for item in dinner_items],
            'calories': cal_d,
            'target': calories_dinner
        },
        'total_calories': cal_b + cal_l + cal_d
    }

def generate_weekly_plan(base_plan):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_plan = []
    
    for day in days:
        daily_plan = {
            'day': day,
            'breakfast': random.sample(base_plan['breakfast']['items'], min(3, len(base_plan['breakfast']['items']))),
            'lunch': random.sample(base_plan['lunch']['items'], min(3, len(base_plan['lunch']['items']))),
            'dinner': random.sample(base_plan['dinner']['items'], min(3, len(base_plan['dinner']['items'])))
        }
        weekly_plan.append(daily_plan)
    
    return weekly_plan

def generate_grocery_list(weekly_plan):
    grocery_list = {}
    for day_plan in weekly_plan:
        for meal_type in ['breakfast', 'lunch', 'dinner']:
            for item in day_plan[meal_type]:
                item_key = item.lower().replace(' ', '_')
                if item_key in grocery_list:
                    grocery_list[item_key] += 1
                else:
                    grocery_list[item_key] = 1
    
    categories = {
        'Proteins': ['chicken', 'beef', 'salmon', 'tofu', 'eggs', 'shrimp', 'paneer', 'dal', 'lentils'],
        'Grains': ['rice', 'quinoa', 'bread', 'pasta', 'oatmeal', 'roti', 'chapati', 'naan'],
        'Vegetables': ['broccoli', 'spinach', 'carrots', 'tomatoes', 'peppers', 'onions', 'cucumber'],
        'Fruits': ['bananas', 'apples', 'berries', 'oranges', 'mango', 'papaya'],
        'Dairy': ['milk', 'yogurt', 'cheese', 'paneer', 'curd'],
        'Others': []
    }
    
    categorized_list = {cat: [] for cat in categories.keys()}
    
    for item, count in grocery_list.items():
        categorized = False
        for category, keywords in categories.items():
            if any(keyword in item.lower() for keyword in keywords):
                categorized_list[category].append({'item': item.replace('_', ' ').title(), 'count': count})
                categorized = True
                break
        if not categorized:
            categorized_list['Others'].append({'item': item.replace('_', ' ').title(), 'count': count})
    
    return categorized_list