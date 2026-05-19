from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import random
import bcrypt
from database import Database
from data import food_database, food_categories, food_items_breakfast, food_items_lunch, food_items_dinner
from functools import wraps
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime, date
from food_therapist import FoodTherapist
from nutrition_optimizer import NutritionOptimizer

# Lazy import - will be loaded only when needed (not at module initialization)
food_model = None
get_food_calories = None

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production

# Initialize database
db = Database()

# Initialize Food Therapist
food_therapist = None

def get_food_therapist():
    global food_therapist
    if food_therapist is None:
        from food_therapist import FoodTherapist
        food_therapist = FoodTherapist()
    return food_therapist

# Initialize Nutrition Optimizer
nutrition_optimizer_instance = None

def get_nutrition_optimizer():
    global nutrition_optimizer_instance
    if nutrition_optimizer_instance is None:
        from nutrition_optimizer import NutritionOptimizer
        nutrition_optimizer_instance = NutritionOptimizer()
    return nutrition_optimizer_instance

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Enhanced food database for snacks
food_items_snacks = {
    "healthy_snacks": {
        "mixed_nuts": 160,
        "greek_yogurt_berries": 120,
        "apple_peanut_butter": 190,
        "protein_bar": 200,
        "hummus_vegetables": 100,
        "cottage_cheese_fruit": 150,
        "trail_mix": 180,
        "protein_smoothie": 220,
        "boiled_eggs": 140,
        "cheese_crackers": 170
    }
}

# Helper Functions
def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender.lower() == "male":
        bmr = 9.99 * weight + 6.25 * height - 4.92 * age + 5
    else:
        bmr = 9.99 * weight + 6.25 * height - 4.92 * age - 161
    return round(bmr, 1)

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Athlete": 1.9
    }
    return round(bmr * activity_multipliers.get(activity_level, 1.2), 1)

def calculate_bmi(weight, height):
    """Calculate Body Mass Index"""
    height_m = height / 100  # Convert cm to meters
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_macros(calories, protein_preference, goal):
    """Calculate macronutrient distribution"""
    # Protein calculation based on preference
    protein_multipliers = {"Low": 0.8, "Medium": 1.2, "High": 1.6}
    protein_per_kg = protein_multipliers.get(protein_preference, 1.2)
    
    # Adjust based on goal
    if goal == "Muscle Gain":
        protein_ratio = 0.30
        carb_ratio = 0.40
        fat_ratio = 0.30
    elif goal == "Weight Loss":
        protein_ratio = 0.35
        carb_ratio = 0.30
        fat_ratio = 0.35
    else:  # Maintenance
        protein_ratio = 0.25
        carb_ratio = 0.45
        fat_ratio = 0.30
    
    protein_calories = calories * protein_ratio
    carb_calories = calories * carb_ratio
    fat_calories = calories * fat_ratio
    
    return {
        "protein": round(protein_calories / 4),  # 4 cal per gram
        "carbs": round(carb_calories / 4),      # 4 cal per gram
        "fats": round(fat_calories / 9)         # 9 cal per gram
    }

def adjust_calories_for_goal(tdee, goal):
    """Adjust calories based on fitness goal"""
    if goal == "Weight Loss":
        return round(tdee - 500)  # 500 cal deficit
    elif goal == "Weight Gain":
        return round(tdee + 500)  # 500 cal surplus
    elif goal == "Muscle Gain":
        return round(tdee + 300)  # 300 cal surplus
    else:  # Maintenance
        return round(tdee)

def generate_health_tips(goal, bmi_category, medical_conditions):
    """Generate personalized health tips"""
    tips = []
    
    # Goal-based tips
    if goal == "Weight Loss":
        tips.extend([
            "Focus on creating a sustainable caloric deficit",
            "Include plenty of fiber-rich foods to stay full",
            "Stay hydrated - sometimes thirst is mistaken for hunger"
        ])
    elif goal == "Muscle Gain":
        tips.extend([
            "Eat protein within 2 hours post-workout",
            "Don't skip meals - consistent nutrition supports muscle growth",
            "Include compound exercises in your workout routine"
        ])
    
    # BMI-based tips
    if bmi_category == "Underweight":
        tips.append("Focus on nutrient-dense, calorie-rich foods")
    elif bmi_category in ["Overweight", "Obese"]:
        tips.append("Prioritize whole foods and limit processed foods")
    
    # Medical condition tips
    if medical_conditions != "None":
        tips.append("Consult with your healthcare provider about your meal plan")
    
    return tips[:4]  # Return max 4 tips

def generate_hydration_tips(activity_level, climate="moderate"):
    """Generate hydration recommendations"""
    base_water = 2.5  # liters
    
    if activity_level in ["Active", "Athlete"]:
        base_water += 1.0
    elif activity_level == "Moderate":
        base_water += 0.5
    
    tips = [
        f"Aim for {base_water:.1f}L of water daily",
        "Drink water before, during, and after workouts",
        "Monitor urine color - pale yellow indicates good hydration",
        "Include water-rich foods like fruits and vegetables"
    ]
    
    return tips

def filter_foods_by_preferences(food_dict, diet_type, allergies):
    filtered_dict = {}
    
    for category, foods in food_dict.items():
        filtered_foods = {}
        for food, calories in foods.items():
            # Diet filtering
            if diet_type == "Vegetarian":
                non_veg_items = ["chicken", "beef", "salmon", "shrimp", "turkey", "smoked_salmon"]
                if any(item in food.lower() for item in non_veg_items):
                    continue
            elif diet_type == "Vegan":
                non_vegan_items = ["chicken", "beef", "salmon", "shrimp", "turkey", "smoked_salmon", 
                                 "eggs", "milk", "cheese", "yogurt", "cottage_cheese", "greek_yogurt"]
                if any(item in food.lower() for item in non_vegan_items):
                    continue
            
            # Allergy filtering
            skip_food = False
            for allergy in allergies:
                if allergy == "Nuts" and ("nut" in food.lower() or "almond" in food.lower()):
                    skip_food = True
                elif allergy == "Dairy" and any(dairy in food.lower() for dairy in ["milk", "cheese", "yogurt"]):
                    skip_food = True
                elif allergy == "Gluten" and any(gluten in food.lower() for gluten in ["wheat", "bread", "pasta", "cereal"]):
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

# Lazy load food model - only initialize when /upload-food-image route is called
def load_food_model():
    """Lazy load the food recognition model only when needed"""
    global food_model
    if food_model is None:
        try:
            from food_recognition import FoodObjectDetectionModel
            food_model = FoodObjectDetectionModel()
            print("✓ Food model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading food model: {str(e)}")
            return None
    return food_model

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'success': False, 'error': 'Email and password required'}), 400
            
            try:
                user = db.get_user_by_email(email)
            except Exception as db_err:
                return jsonify({'success': False, 'error': f'Database error: {str(db_err)}'}), 500
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
                session['user_email'] = email
                session['user_name'] = f"{user['first_name']} {user['last_name']}"
                session.permanent = True
                try:
                    db.update_last_login(email)
                except Exception as db_err:
                    pass  # Non-critical
                return jsonify({'success': True, 'redirect': '/dashboard'})
            else:
                return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        except Exception as e:
            return jsonify({'success': False, 'error': f'Login error: {str(e)}'}), 500
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            
            # Validation
            if not all([email, password, first_name, last_name]):
                return jsonify({'success': False, 'error': 'All fields required'}), 400
            
            # Check if user already exists
            try:
                existing_user = db.get_user_by_email(email)
                if existing_user:
                    return jsonify({'success': False, 'error': 'Email already registered'}), 409
            except Exception as db_err:
                return jsonify({'success': False, 'error': f'Database error: {str(db_err)}'}), 500
            
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user
            try:
                db.create_user(email, password_hash, first_name, last_name)
                session['user_email'] = email
                session['user_name'] = f"{first_name} {last_name}"
                session.permanent = True
                return jsonify({'success': True, 'redirect': '/dashboard'})
            except Exception as db_err:
                return jsonify({'success': False, 'error': f'Registration failed: {str(db_err)}'}), 500
        except Exception as e:
            return jsonify({'success': False, 'error': f'Signup error: {str(e)}'}), 500
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        user_email = session.get('user_email')
        user = db.get_user_by_email(user_email) if user_email else None
        
        # Get today's summary
        today_summary = db.get_today_summary(user_email) if user_email else {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        if not today_summary:
            today_summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        # Get today's meals - ensure it's always a dictionary
        today_meals = {}
        if user_email:
            meals_data = db.get_today_meals(user_email)
            if meals_data:
                # Serialize meals to convert ObjectIds to strings
                today_meals = db._serialize_meals_for_json(meals_data)
            else:
                today_meals = {'breakfast': [], 'lunch': [], 'snack': [], 'dinner': []}
        else:
            today_meals = {'breakfast': [], 'lunch': [], 'snack': [], 'dinner': []}
        
        return render_template('dashboard.html', 
                             user_name=session.get('user_name'),
                             user=user,
                             today_summary=today_summary,
                             today_meals=today_meals,
                             daily_goals={
                                 'calories': user.get('daily_calorie_goal', 2000) if user else 2000,
                                 'protein': user.get('daily_protein_goal', 50) if user else 50,
                                 'carbs': user.get('daily_carbs_goal', 300) if user else 300,
                                 'fat': user.get('daily_fat_goal', 65) if user else 65
                             })
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('dashboard.html', 
                             user_name=session.get('user_name'),
                             today_meals={'breakfast': [], 'lunch': [], 'snack': [], 'dinner': []},
                             today_summary={'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0},
                             daily_goals={'calories': 2000, 'protein': 50, 'carbs': 300, 'fat': 65})

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from Food Therapist
        therapist = get_food_therapist()
        response = therapist.chat(user_message)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat_message: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/optimize-nutrition', methods=['POST'])
def optimize_nutrition():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        # Extract parameters
        daily_calories = data.get('daily_calories', 2000)
        weekly_budget = data.get('weekly_budget', 1000)
        goal = data.get('goal', 'maintenance')
        weight = data.get('weight', 70)
        age = data.get('age', 30)  # Default to 30 if not provided
        deficiencies = data.get('deficiencies', [])
        diet_preference = data.get('diet_preference', 'veg')

        # Validate inputs
        if not isinstance(daily_calories, (int, float)) or daily_calories < 1000 or daily_calories > 5000:
            return jsonify({'error': 'Daily calories must be between 1000 and 5000'}), 400

        if not isinstance(weekly_budget, (int, float)) or weekly_budget < 500 or weekly_budget > 10000:
            return jsonify({'error': 'Weekly budget must be between ₹500 and ₹10000'}), 400

        if not isinstance(weight, (int, float)) or weight < 30 or weight > 200:
            return jsonify({'error': 'Weight must be between 30kg and 200kg'}), 400

        if goal.lower() not in ['weight loss', 'maintenance', 'muscle gain']:
            return jsonify({'error': 'Goal must be weight loss, maintenance, or muscle gain'}), 400

        if diet_preference.lower() not in ['veg', 'non-veg']:
            return jsonify({'error': 'Diet preference must be veg or non-veg'}), 400

        # Get optimized plan
        optimizer = get_nutrition_optimizer()
        plan = optimizer.optimize_grocery_plan(
            daily_calories=daily_calories,
            weekly_budget=weekly_budget,
            goal=goal,
            weight=weight,
            age=age,
            deficiencies=deficiencies,
            diet_preference=diet_preference
        )

        # Format the plan for display
        formatted_plan = optimizer.format_grocery_plan(plan)

        return jsonify({
            'plan': plan,
            'formatted_plan': formatted_plan
        })

    except Exception as e:
        print(f"Error in optimize_nutrition: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/nutrition-optimizer')
def nutrition_optimizer():
    return render_template('nutrition_optimizer.html')

@app.route('/admin')
def admin():
    stats = {
        'total_users': 1247,
        'total_plans': 3891,
        'today_plans': 47,
        'active_users': 892
    }
    
    users = [
        {'id': 1, 'email': 'user1@example.com', 'joined': '2024-01-15'},
        {'id': 2, 'email': 'user2@example.com', 'joined': '2024-01-14'},
        {'id': 3, 'email': 'user3@example.com', 'joined': '2024-01-13'}
    ]
    
    meal_plans = [
        {'user_email': 'user1@example.com', 'goal': 'Weight Loss', 'calories': 1800, 'created_at': '2024-01-15'},
        {'user_email': 'user2@example.com', 'goal': 'Muscle Gain', 'calories': 2500, 'created_at': '2024-01-15'},
        {'user_email': 'user3@example.com', 'goal': 'Maintenance', 'calories': 2200, 'created_at': '2024-01-14'}
    ]
    
    return render_template('admin.html', stats=stats, users=users, meal_plans=meal_plans)

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/help')
def help_center():
    return render_template('help.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/food-upload')
def food_upload():
    return render_template('food-upload.html')

@app.route('/upload-food-image', methods=['POST'])
def upload_food_image():
    try:
        # Check if file is present
        if 'food_image' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['food_image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Validate file type and size
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload JPG or PNG files only.'})
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'success': False, 'error': 'File size too large. Maximum 5MB allowed.'})
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Lazy load the food model if not already loaded
        model = load_food_model()
        if model is None:
            return jsonify({'success': False, 'error': 'Food recognition model could not be loaded'})
        
        # Detect multiple food items using object detection
        detection_result = model.detect_foods(file_path, conf_threshold=0.5)
        
        # Clean up - remove uploaded file after processing
        try:
            os.remove(file_path)
        except:
            pass  # File cleanup is not critical
        
        if detection_result['success']:
            return jsonify({
                'success': True,
                'detections': detection_result['detections'],
                'image_with_boxes': detection_result['image_with_boxes'],
                'total_detections': detection_result['total_detections'],
                'food_counts': detection_result['food_counts'],
                'nutrition_summary': detection_result['nutrition_summary'],
                'total_calories': detection_result['total_calories'],
                'image_dimensions': detection_result['image_dimensions']
            })
        else:
            return jsonify({
                'success': False,
                'error': detection_result.get('error', 'Failed to detect food items')
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error processing image: {str(e)}'
        }), 500



def get_food_calories(food_name):
    """Get calories for a specific food item"""
    all_foods = {**food_items_breakfast, **food_items_lunch, **food_items_dinner, **food_items_snacks}
    for category in all_foods.values():
        if food_name in category:
            return category[food_name]
    return 0

def calculate_meal_macros(meal_calories, daily_macros, daily_calories):
    """Calculate macros for individual meal based on proportion"""
    proportion = meal_calories / daily_calories if daily_calories > 0 else 0
    return {
        "protein": round(daily_macros["protein"] * proportion),
        "carbs": round(daily_macros["carbs"] * proportion),
        "fats": round(daily_macros["fats"] * proportion)
    }

# ============ FOOD TRACKING ROUTES ============

@app.route('/track')
@login_required
def track():
    """Food tracking page"""
    try:
        user_email = session['user_email']
        user = db.get_user_by_email(user_email)
        
        # Get today's meals and summary
        today_meals = db.get_today_meals(user_email)
        today_summary = db.get_today_summary(user_email)
        
        # Get all foods for autocomplete
        all_foods = db.get_all_foods()
        
        return render_template('track.html', 
                             user_name=session.get('user_name'),
                             today_meals=today_meals,
                             today_summary=today_summary,
                             all_foods=all_foods,
                             daily_goals={
                                 'calories': user.get('daily_calorie_goal', 2000) if user else 2000,
                                 'protein': user.get('daily_protein_goal', 50) if user else 50,
                                 'carbs': user.get('daily_carbs_goal', 300) if user else 300,
                                 'fat': user.get('daily_fat_goal', 65) if user else 65
                             })
    except Exception as e:
        flash(f'Error loading tracking page: {str(e)}', 'error')
        return render_template('track.html', user_name=session.get('user_name'), daily_goals={
            'calories': 2000, 'protein': 50, 'carbs': 300, 'fat': 65
        })

@app.route('/api/add_food', methods=['POST'])
def add_food():
    """Add food to a meal (AJAX)"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
        
        user_email = session['user_email']
        meal_type = data.get('meal_type')
        food_name = data.get('food_name')
        quantity = float(data.get('quantity', 100))
        portion_type = data.get('portion_type', 'g')
        
        # Validate inputs
        if not all([meal_type, food_name, quantity]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Add food to meal
        food_log_id = db.add_food_to_meal(user_email, meal_type, food_name, quantity, portion_type)
        
        if not food_log_id:
            return jsonify({'success': False, 'error': 'Food not found in database'}), 404
        
        # Get updated meals and summary
        today_meals = db.get_today_meals(user_email)
        today_summary = db.get_today_summary(user_email)
        if not today_summary:
            today_summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        return jsonify({
            'success': True,
            'food_log_id': str(food_log_id),
            'today_meals': db._serialize_meals_for_json(today_meals),
            'today_summary': today_summary
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Invalid quantity: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500

@app.route('/api/remove_food/<food_log_id>', methods=['DELETE'])
def remove_food(food_log_id):
    """Remove food from a meal (AJAX)"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        user_email = session['user_email']
        
        if not food_log_id:
            return jsonify({'success': False, 'error': 'Food ID required'}), 400
        
        # Remove food
        success = db.remove_food_from_meal(food_log_id)
        
        if not success:
            return jsonify({'success': False, 'error': 'Food log not found'}), 404
        
        # Get updated meals and summary
        today_meals = db.get_today_meals(user_email)
        today_summary = db.get_today_summary(user_email)
        if not today_summary:
            today_summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        return jsonify({
            'success': True,
            'today_meals': db._serialize_meals_for_json(today_meals),
            'today_summary': today_summary
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500

@app.route('/api/search_foods', methods=['GET'])
def search_foods():
    """Search foods in database (AJAX)"""
    try:
        query = request.args.get('q', '')
        
        if len(query) < 2:
            return jsonify([])
        
        results = db.search_foods(query)
        
        # Format results
        formatted_results = []
        for food in results:
            formatted_results.append({
                'id': str(food.get('_id', '')),
                'name': food['name'],
                'calories': food['calories'],
                'protein': food['protein'],
                'carbs': food['carbs'],
                'fat': food['fat'],
                'portion_size': food['portion_size'],
                'portion_unit': food['portion_unit']
            })
        
        return jsonify(formatted_results)
    
    except Exception as e:
        return jsonify({'error': f'Search error: {str(e)}'}), 500

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    try:
        user_email = session['user_email']
        user = db.get_user_by_email(user_email)
        
        # Get today's summary
        today_summary = db.get_today_summary(user_email)
        if not today_summary:
            today_summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        # Get today's meals
        today_meals = db.get_today_meals(user_email)
        
        return render_template('profile.html',
                             user_name=session.get('user_name'),
                             user=user,
                             today_summary=today_summary,
                             today_meals=today_meals)
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'error')
        return render_template('profile.html',
                             user_name=session.get('user_name'),
                             user=None,
                             today_summary={'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0},
                             today_meals={})

@app.route('/api/update_goals', methods=['POST'])
def update_goals():
    """Update daily nutritional goals (AJAX)"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
        
        user_email = session['user_email']
        
        # Validate required fields and types
        try:
            daily_calorie_goal = int(data.get('daily_calorie_goal', 2000))
            daily_protein_goal = int(data.get('daily_protein_goal', 50))
            daily_carbs_goal = int(data.get('daily_carbs_goal', 300))
            daily_fat_goal = int(data.get('daily_fat_goal', 65))
            
            if any(x < 0 for x in [daily_calorie_goal, daily_protein_goal, daily_carbs_goal, daily_fat_goal]):
                return jsonify({'success': False, 'error': 'Goals must be non-negative'}), 400
        
        except ValueError:
            return jsonify({'success': False, 'error': 'Goals must be numbers'}), 400
        
        # Validate and update goals
        profile_update = {
            'daily_calorie_goal': daily_calorie_goal,
            'daily_protein_goal': daily_protein_goal,
            'daily_carbs_goal': daily_carbs_goal,
            'daily_fat_goal': daily_fat_goal
        }
        
        db.update_user_profile(user_email, profile_update)
        
        return jsonify({'success': True, 'message': 'Goals updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Update error: {str(e)}'}), 500

@app.route('/api/profile_data', methods=['GET'])
def profile_data():
    """Get profile data for profile page (AJAX)"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        user_email = session['user_email']
        user = db.get_user_by_email(user_email)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Get today's summary
        today_summary = db.get_today_summary(user_email)
        if not today_summary:
            today_summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        # Get today's meals
        today_meals = db.get_today_meals(user_email)
        
        return jsonify({
            'success': True,
            'user_name': session.get('user_name', ''),
            'email': user_email,
            'created_at': str(user.get('created_at', '')),
            'today_summary': today_summary,
            'today_meals': db._serialize_meals_for_json(today_meals),
            'daily_goals': {
                'daily_calorie_goal': user.get('daily_calorie_goal', 2000),
                'daily_protein_goal': user.get('daily_protein_goal', 50),
                'daily_carbs_goal': user.get('daily_carbs_goal', 300),
                'daily_fat_goal': user.get('daily_fat_goal', 65)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Profile error: {str(e)}'}), 500

@app.route('/api/today_meals', methods=['GET'])
def api_today_meals():
    """Get today's meals and summary (AJAX)"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        user_email = session['user_email']
        
        # Get today's meals and summary
        meals = db.get_today_meals(user_email)
        summary = db.get_today_summary(user_email)
        if not summary:
            summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        return jsonify({
            'success': True,
            'meals': db._serialize_meals_for_json(meals) if meals else [],
            'summary': summary
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Meals error: {str(e)}'}), 500

@app.route('/api/analyze-nutrition', methods=['POST'])
@login_required
def analyze_nutrition():
    """Analyze daily nutrition intake and provide personalized insights"""
    try:
        user_email = session['user_email']
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400

        # Get user profile data
        user = db.get_user_by_email(user_email)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Use safe defaults for user data
        weight = user.get('weight', 70) or 70
        age = user.get('age', 30) or 30
        goal = user.get('fitness_goal', 'maintenance') or 'maintenance'

        # Prepare analysis data
        analysis_data = {
            'calories': data.get('calories', 0),
            'protein': data.get('protein', 0),
            'carbs': data.get('carbs', 0),
            'fats': data.get('fats', 0),
            'sugar': data.get('sugar', 0),
            'fiber': data.get('fiber', 0),
            'sodium': data.get('sodium', 0),
            'water': data.get('water', 0),
            'weight': weight,
            'age': age,
            'goal': goal,
            'meals': data.get('meals', [])
        }

        # Debug: print analysis data
        print(f"Analysis data: {analysis_data}")

        # Get nutrition insights
        optimizer = get_nutrition_optimizer()
        insights = optimizer.analyze_daily_intake(analysis_data)

        return jsonify({
            'success': True,
            'insights': insights,
            'analysis_data': analysis_data
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': f'Analysis error: {str(e)}'}), 500

# ============ AI MEAL PLANNER ROUTES ============

@app.route('/meal-planner')
@login_required
def meal_planner():
    """AI Meal Planner page"""
    try:
        user_email = session.get('user_email')
        user = db.get_user_by_email(user_email) if user_email else None
        
        return render_template('ai_meal_planner.html', 
                             user_name=session.get('user_name'),
                             user=user)
    except Exception as e:
        flash(f'Error loading meal planner: {str(e)}', 'error')
        return render_template('ai_meal_planner.html', user_name=session.get('user_name'))

@app.route('/api/generate-meal-plan', methods=['POST'])
@login_required
def generate_meal_plan():
    """Generate AI meal plan based on user profile"""
    try:
        user_email = session['user_email']
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400
        
        # Extract user inputs
        age = int(data.get('age', 25))
        weight = float(data.get('weight', 70))
        height = float(data.get('height', 170))
        gender = data.get('gender', 'male')
        activity_level = data.get('activity_level', 'moderate')
        goal = data.get('goal', 'maintain')
        
        # Calculate daily calorie needs
        daily_calories = calculate_daily_calories(weight, height, age, gender, activity_level, goal)
        
        # Generate meal plan
        meal_plan = generate_ai_meal_plan(daily_calories, goal)
        
        # Save meal plan to database
        plan_data = {
            'user_email': user_email,
            'date': date.today().isoformat(),
            'user_inputs': {
                'age': age,
                'weight': weight,
                'height': height,
                'gender': gender,
                'activity_level': activity_level,
                'goal': goal
            },
            'daily_calories': daily_calories,
            'meal_plan': meal_plan,
            'created_at': datetime.utcnow()
        }
        
        plan_id = db.save_meal_plan(user_email, plan_data)
        
        return jsonify({
            'success': True,
            'plan_id': str(plan_id),
            'daily_calories': daily_calories,
            'meal_plan': meal_plan
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Generation error: {str(e)}'}), 500

@app.route('/api/add-meal-to-tracking/<meal_type>', methods=['POST'])
@login_required
def add_meal_to_tracking(meal_type):
    """Add generated meal to food tracking"""
    try:
        user_email = session['user_email']
        data = request.get_json()
        
        if not data or 'meal_plan' not in data:
            return jsonify({'success': False, 'error': 'Meal plan data required'}), 400
        
        meal_plan = data['meal_plan']
        if meal_type not in meal_plan:
            return jsonify({'success': False, 'error': f'Meal type {meal_type} not found'}), 404
        
        # Add each food item to tracking
        added_items = []
        for food_item in meal_plan[meal_type]['foods']:
            food_log_id = db.add_food_to_meal(
                user_email=user_email,
                meal_type=meal_type,
                food_name=food_item['name'],
                quantity=food_item['quantity'],
                portion_type=food_item['portion_type']
            )
            if food_log_id:
                added_items.append(str(food_log_id))
        
        if added_items:
            return jsonify({
                'success': True,
                'message': f'Added {len(added_items)} items to {meal_type}',
                'added_items': added_items
            })
        else:
            return jsonify({'success': False, 'error': 'No items could be added'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error adding to tracking: {str(e)}'}), 500

# ============ AI MEAL PLANNER HELPER FUNCTIONS ============

def calculate_daily_calories(weight, height, age, gender, activity_level, goal):
    """Calculate daily calorie needs based on user profile"""
    # Calculate BMR
    bmr = calculate_bmr(weight, height, age, gender)
    
    # Apply activity level multiplier
    activity_multipliers = {
        'low': 1.2,      # Sedentary
        'moderate': 1.55, # Lightly active
        'high': 1.725    # Very active
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    
    # Adjust based on goal
    if goal == 'weight_loss':
        daily_calories = tdee - 500  # 500 calorie deficit
    elif goal == 'weight_gain':
        daily_calories = tdee + 500  # 500 calorie surplus
    else:  # maintain
        daily_calories = tdee
    
    return max(int(daily_calories), 1200)  # Minimum 1200 calories

def generate_ai_meal_plan(daily_calories, goal='maintain'):
    """Generate AI meal plan with balanced nutrition based on goal"""
    # Define meal calorie distribution: 30% breakfast, 40% lunch, 30% dinner
    breakfast_calories = int(daily_calories * 0.30)
    lunch_calories = int(daily_calories * 0.40)
    dinner_calories = daily_calories - breakfast_calories - lunch_calories  # Ensure exact total

    # Generate meals with goal-based logic
    breakfast = generate_meal('breakfast', breakfast_calories, goal)
    lunch = generate_meal('lunch', lunch_calories, goal)
    dinner = generate_meal('dinner', dinner_calories, goal)

    return {
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner
    }

def generate_meal(meal_type, target_calories, goal='maintain'):
    """Generate a nutritionally balanced meal within calorie limits based on goal"""

    # Goal-based food selection strategy
    if goal == 'weight_loss':
        preferred_proteins = ['eggs', 'chicken_breast', 'fish', 'salmon', 'tuna', 'paneer', 'tofu', 'lentils', 'chickpeas', 'moong_dal', 'sprouts', 'greek_yogurt', 'cottage_cheese']
        preferred_carbs = ['brown_rice', 'quinoa', 'oats', 'whole_wheat_roti', 'multigrain_roti', 'barley', 'millet', 'jowar', 'bajra', 'ragi']
        preferred_veggies = ['spinach', 'broccoli', 'carrots', 'bell_peppers', 'tomatoes', 'cucumber', 'lettuce', 'cabbage', 'cauliflower', 'green_beans', 'okra', 'eggplant', 'zucchini', 'beetroot']
        preferred_fats = ['avocado', 'olive_oil', 'nuts', 'almonds', 'chia_seeds', 'flaxseeds']
        include_dairy = ['curd', 'greek_yogurt']

    elif goal == 'weight_gain':
        preferred_proteins = ['chicken_breast', 'chicken_thigh', 'fish', 'salmon', 'paneer', 'eggs', 'greek_yogurt', 'cottage_cheese']
        preferred_carbs = ['brown_rice', 'quinoa', 'oats', 'whole_wheat_roti', 'whole_grain_pasta', 'bajra', 'jowar', 'amaranth']
        preferred_veggies = ['sweet_potato', 'peas', 'potato', 'carrots', 'beetroot', 'avocado']
        preferred_fats = ['avocado', 'olive_oil', 'ghee', 'nuts', 'walnuts', 'peanuts', 'chia_seeds']
        include_dairy = ['milk', 'yogurt', 'curd', 'lassi']

    else:  # maintain
        preferred_proteins = ['eggs', 'chicken_breast', 'fish', 'paneer', 'tofu', 'lentils', 'chickpeas']
        preferred_carbs = ['brown_rice', 'quinoa', 'oats', 'whole_wheat_roti', 'whole_grain_pasta']
        preferred_veggies = ['broccoli', 'spinach', 'carrots', 'bell_peppers', 'tomatoes', 'cucumber']
        preferred_fats = ['avocado', 'olive_oil', 'nuts', 'almonds']
        include_dairy = ['curd', 'yogurt']

    # Meal structure based on meal type
    if meal_type == 'breakfast':
        # Breakfast: 1 protein + 1 carb + 1-2 veggies + optional dairy
        food_lists = [preferred_proteins, preferred_carbs, preferred_veggies]
        if random.random() < 0.7:
            food_lists.append(include_dairy)
        if random.random() < 0.4 and goal != 'weight_loss':
            food_lists.append(preferred_fats)

    elif meal_type == 'lunch':
        # Lunch: 1 protein + 1 carb + 2 veggies + optional fat + optional dairy
        food_lists = [preferred_proteins, preferred_carbs, preferred_veggies, preferred_veggies]
        if random.random() < 0.6:
            food_lists.append(preferred_fats)
        if random.random() < 0.5:
            food_lists.append(include_dairy)

    else:  # dinner
        # Dinner: 1 protein + 1 carb + 2 veggies + optional fat
        food_lists = [preferred_proteins, preferred_carbs, preferred_veggies, preferred_veggies]
        if random.random() < 0.5:
            food_lists.append(preferred_fats)
        if random.random() < 0.4 and goal != 'weight_gain':
            food_lists.append(include_dairy)

    # Select foods and calculate portions to meet calorie target
    selected_foods = []
    total_calories = 0
    max_attempts = 10

    for attempt in range(max_attempts):
        selected_foods = []
        total_calories = 0

        # Select one food from each category
        for food_list in food_lists:
            available_foods = [f for f in food_list if f in food_database]
            if not available_foods:
                continue

            food_name = random.choice(available_foods)
            food_data = food_database[food_name]
            base_calories = food_data[0]
            portion_size = food_data[5]

            # Start with base portion
            quantity = portion_size
            calories = base_calories

            food_item = {
                'name': food_name.replace('_', ' ').title(),
                'quantity': round(quantity, 1),
                'portion_type': food_data[6],
                'calories': round(calories, 1),
                'protein': round((food_data[1] / portion_size) * quantity, 1),
                'carbs': round((food_data[2] / portion_size) * quantity, 1),
                'fat': round((food_data[3] / portion_size) * quantity, 1)
            }

            selected_foods.append(food_item)
            total_calories += calories

        # Scale portions to meet calorie target
        if selected_foods and total_calories > 0:
            scale_factor = target_calories / total_calories

            # Apply scaling but limit to reasonable ranges
            if goal == 'weight_loss':
                scale_factor = min(1.8, max(0.7, scale_factor))  # Allow more scaling for weight loss
            elif goal == 'weight_gain':
                scale_factor = min(2.2, max(0.8, scale_factor))  # Allow more scaling for weight gain
            else:
                scale_factor = min(2.0, max(0.8, scale_factor))  # Moderate scaling for maintain

            # Recalculate with scaling
            total_calories = 0
            for food_item in selected_foods:
                food_name = food_item['name'].lower().replace(' ', '_')
                if food_name in food_database:
                    food_data = food_database[food_name]
                    base_calories = food_data[0]
                    portion_size = food_data[5]

                    new_quantity = food_item['quantity'] * scale_factor
                    new_calories = (base_calories / portion_size) * new_quantity

                    food_item['quantity'] = round(new_quantity, 1)
                    food_item['calories'] = round(new_calories, 1)
                    food_item['protein'] = round((food_data[1] / portion_size) * new_quantity, 1)
                    food_item['carbs'] = round((food_data[2] / portion_size) * new_quantity, 1)
                    food_item['fat'] = round((food_data[3] / portion_size) * new_quantity, 1)

                    total_calories += new_calories

        # Check if we're close enough to target (within 10%)
        if abs(total_calories - target_calories) / target_calories <= 0.1:
            break

    # If we're still under target significantly, add more food
    if total_calories < target_calories * 0.9 and len(selected_foods) < 6:
        # Add another vegetable or carb
        extra_options = preferred_veggies + preferred_carbs
        available_foods = [f for f in extra_options if f in food_database]
        if available_foods:
            food_name = random.choice(available_foods)
            food_data = food_database[food_name]
            base_calories = food_data[0]
            portion_size = food_data[5]

            # Calculate how much more we need
            needed_calories = target_calories - total_calories
            quantity = min(portion_size * 2, (needed_calories / base_calories) * portion_size)

            calories = (base_calories / portion_size) * quantity
            protein = (food_data[1] / portion_size) * quantity
            carbs = (food_data[2] / portion_size) * quantity
            fat = (food_data[3] / portion_size) * quantity

            if total_calories + calories <= target_calories * 1.2:  # Don't exceed too much
                food_item = {
                    'name': food_name.replace('_', ' ').title(),
                    'quantity': round(quantity, 1),
                    'portion_type': food_data[6],
                    'calories': round(calories, 1),
                    'protein': round(protein, 1),
                    'carbs': round(carbs, 1),
                    'fat': round(fat, 1)
                }

                selected_foods.append(food_item)
                total_calories += calories

    # Calculate total nutrition
    total_protein = sum(food['protein'] for food in selected_foods)
    total_carbs = sum(food['carbs'] for food in selected_foods)
    total_fat = sum(food['fat'] for food in selected_foods)

    return {
        'foods': selected_foods,
        'total_calories': round(total_calories, 1),
        'total_protein': round(total_protein, 1),
        'total_carbs': round(total_carbs, 1),
        'total_fat': round(total_fat, 1)
    }

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)