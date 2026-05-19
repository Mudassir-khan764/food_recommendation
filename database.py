from pymongo import MongoClient
from datetime import datetime, date
import os
from bson.objectid import ObjectId

class Database:
    def __init__(self):
        # MongoDB connection - using local MongoDB for development
        # Added serverSelectionTimeoutMS to prevent hanging
        try:
            self.client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
        except Exception as e:
            print(f"Warning: MongoDB connection may have issues: {e}")
            self.client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        self.db = self.client['meal_planner']
        
        # Collections
        self.users = self.db['users']
        self.meal_plans = self.db['meal_plans']
        self.foods = self.db['foods']  # Food database with nutrition info
        self.food_logs = self.db['food_logs']  # User's food tracking logs
        self.daily_summary = self.db['daily_summary']  # Daily nutrition totals
    
    # ============ USER OPERATIONS ============
    def create_user(self, email, password_hash, first_name, last_name):
        """Create a new user"""
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'first_name': first_name,
            'last_name': last_name,
            'age': None,
            'gender': None,
            'weight': None,
            'height': None,
            'daily_calorie_goal': 2000,  # Default
            'daily_protein_goal': 50,    # Default grams
            'daily_carbs_goal': 300,     # Default grams
            'daily_fat_goal': 65,        # Default grams
            'created_at': datetime.utcnow(),
            'last_login': None
        }
        return self.users.insert_one(user_data)
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return self.users.find_one({'email': email})
    
    def update_user_profile(self, email, profile_data):
        """Update user profile (goals, demographics)"""
        return self.users.update_one(
            {'email': email},
            {'$set': profile_data}
        )
    
    def update_last_login(self, email):
        """Update user's last login time"""
        return self.users.update_one(
            {'email': email},
            {'$set': {'last_login': datetime.utcnow()}}
        )
    
    # ============ MEAL PLAN OPERATIONS ============
    def save_meal_plan(self, user_email, meal_plan_data):
        """Save user's meal plan"""
        meal_plan = {
            'user_email': user_email,
            'meal_plan': meal_plan_data,
            'created_at': datetime.utcnow()
        }
        return self.meal_plans.insert_one(meal_plan)
    
    def get_user_meal_plans(self, user_email, limit=10):
        """Get user's meal plan history"""
        return list(self.meal_plans.find(
            {'user_email': user_email}
        ).sort('created_at', -1).limit(limit))
    
    # ============ FOOD DATABASE OPERATIONS ============
    def add_food(self, food_name, calories, protein, carbs, fat, portion_size=100, portion_unit='g'):
        """Add a food to the food database"""
        food_data = {
            'name': food_name.lower(),
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat,
            'portion_size': portion_size,
            'portion_unit': portion_unit,
            'created_at': datetime.utcnow()
        }
        # Check if already exists
        existing = self.foods.find_one({'name': food_name.lower()})
        if existing:
            return existing['_id']
        return self.foods.insert_one(food_data).inserted_id
    
    def get_food(self, food_name):
        """Get food by name"""
        return self.foods.find_one({'name': food_name.lower()})
    
    def get_all_foods(self):
        """Get all foods in database"""
        return list(self.foods.find())
    
    def _serialize_food_for_json(self, food):
        """Convert food document to JSON-serializable format"""
        if food is None:
            return None
        if '_id' in food:
            food['_id'] = str(food['_id'])
        return food
    
    def _serialize_meals_for_json(self, meals):
        """Convert meals dictionary with ObjectIds to JSON-serializable format"""
        serialized = {}
        for meal_type, foods in meals.items():
            serialized[meal_type] = [self._serialize_food_for_json(f) for f in foods]
        return serialized
    
    def search_foods(self, query):
        """Search foods by name"""
        return list(self.foods.find({
            'name': {'$regex': query.lower(), '$options': 'i'}
        }).limit(10))
    
    # ============ FOOD LOGGING OPERATIONS ============
    def add_food_to_meal(self, user_email, meal_type, food_name, quantity, portion_type='g'):
        """Add food to a specific meal for today"""
        today = date.today().isoformat()
        
        # Get food from database
        food = self.get_food(food_name)
        if not food:
            return None
        
        # Calculate nutrition based on quantity
        multiplier = quantity / food['portion_size']
        food_log = {
            'user_email': user_email,
            'date': today,
            'meal_type': meal_type.lower(),  # breakfast, lunch, snack, dinner
            'food_name': food_name,
            'quantity': quantity,
            'portion_type': portion_type,
            'calories': round(food['calories'] * multiplier, 2),
            'protein': round(food['protein'] * multiplier, 2),
            'carbs': round(food['carbs'] * multiplier, 2),
            'fat': round(food['fat'] * multiplier, 2),
            'logged_at': datetime.utcnow()
        }
        result = self.food_logs.insert_one(food_log)
        
        # Update daily summary
        self._update_daily_summary(user_email, today)
        
        return result.inserted_id
    
    def remove_food_from_meal(self, food_log_id):
        """Remove food from a meal"""
        # Get the food log to find the user and date
        food_log = self.food_logs.find_one({'_id': ObjectId(food_log_id)})
        if not food_log:
            return False
        
        user_email = food_log['user_email']
        today = food_log['date']
        
        # Delete the food log
        self.food_logs.delete_one({'_id': ObjectId(food_log_id)})
        
        # Update daily summary
        self._update_daily_summary(user_email, today)
        
        return True
    
    def get_today_meals(self, user_email):
        """Get all meals for today"""
        today = date.today().isoformat()
        foods = list(self.food_logs.find({
            'user_email': user_email,
            'date': today
        }).sort('logged_at', 1))
        
        # Organize by meal type
        meals = {
            'breakfast': [],
            'lunch': [],
            'snack': [],
            'dinner': []
        }
        
        for food in foods:
            meal_type = food.get('meal_type', 'snack')
            if meal_type in meals:
                meals[meal_type].append(food)
        
        return meals
    
    def get_meal_totals(self, user_email, date_str):
        """Get totals for a specific meal"""
        foods = list(self.food_logs.find({
            'user_email': user_email,
            'date': date_str
        }))
        
        totals = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0
        }
        
        for food in foods:
            totals['calories'] += food.get('calories', 0)
            totals['protein'] += food.get('protein', 0)
            totals['carbs'] += food.get('carbs', 0)
            totals['fat'] += food.get('fat', 0)
        
        return totals
    
    def _update_daily_summary(self, user_email, date_str):
        """Update daily summary totals"""
        totals = self.get_meal_totals(user_email, date_str)
        
        summary = {
            'user_email': user_email,
            'date': date_str,
            'calories': round(totals['calories'], 2),
            'protein': round(totals['protein'], 2),
            'carbs': round(totals['carbs'], 2),
            'fat': round(totals['fat'], 2),
            'updated_at': datetime.utcnow()
        }
        
        # Upsert - update if exists, insert if not
        self.daily_summary.update_one(
            {'user_email': user_email, 'date': date_str},
            {'$set': summary},
            upsert=True
        )
    
    def get_today_summary(self, user_email):
        """Get today's nutrition summary"""
        today = date.today().isoformat()
        summary = self.daily_summary.find_one({
            'user_email': user_email,
            'date': today
        })
        
        if not summary:
            return {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }
        
        return {
            'calories': summary.get('calories', 0),
            'protein': summary.get('protein', 0),
            'carbs': summary.get('carbs', 0),
            'fat': summary.get('fat', 0)
        }