import streamlit as st
import pandas as pd
import requests
import random
import time
import math
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from data import food_items_breakfast, food_items_lunch, food_items_dinner
from prompts import pre_prompt_b, pre_prompt_l, pre_prompt_d, pre_breakfast, pre_lunch, pre_dinner, end_text, \
    example_response_l, example_response_d, negative_prompt

UNITS_CM_TO_IN = 0.393701
UNITS_KG_TO_LB = 2.20462
UNITS_LB_TO_KG = 0.453592
UNITS_IN_TO_CM = 2.54

# Configure Groq API
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}

# Disable SSL verification warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(
    page_title="NutriAI - Smart Meal Planner", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .success-card {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .warning-card {
        background: linear-gradient(45deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        bmr = 9.99 * weight + 6.25 * height - 4.92 * age + 5
    else:
        bmr = 9.99 * weight + 6.25 * height - 4.92 * age - 161
    return bmr

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        "Sedentary (office job)": 1.2,
        "Lightly Active (light exercise 1-3 days/week)": 1.375,
        "Moderately Active (moderate exercise 3-5 days/week)": 1.55,
        "Very Active (hard exercise 6-7 days/week)": 1.725,
        "Extremely Active (very hard exercise, physical job)": 1.9
    }
    return bmr * activity_multipliers[activity_level]

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return bmi

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "🔵", "#3498db"
    elif 18.5 <= bmi < 25:
        return "Normal weight", "🟢", "#2ecc71"
    elif 25 <= bmi < 30:
        return "Overweight", "🟡", "#f39c12"
    else:
        return "Obese", "🔴", "#e74c3c"

def calculate_water_intake(weight, activity_level, climate="temperate"):
    base_water = weight * 35  # ml per kg
    if "Very Active" in activity_level or "Extremely Active" in activity_level:
        base_water += 500
    elif "Moderately Active" in activity_level:
        base_water += 250
    
    if climate == "hot":
        base_water += 300
    elif climate == "cold":
        base_water -= 200
        
    return max(base_water / 1000, 1.5)  # Convert to liters, minimum 1.5L

def adjust_calories_for_goal(tdee, goal, intensity="moderate"):
    adjustments = {
        "Weight Loss": {"moderate": -500, "aggressive": -750, "conservative": -300},
        "Weight Gain": {"moderate": 500, "aggressive": 750, "conservative": 300},
        "Muscle Gain": {"moderate": 300, "aggressive": 500, "conservative": 200},
        "Maintenance": {"moderate": 0, "aggressive": 0, "conservative": 0}
    }
    return tdee + adjustments[goal][intensity]

def calculate_macros(calories, goal):
    if goal == "Muscle Gain":
        protein_ratio, carb_ratio, fat_ratio = 0.30, 0.40, 0.30
    elif goal == "Weight Loss":
        protein_ratio, carb_ratio, fat_ratio = 0.35, 0.35, 0.30
    else:
        protein_ratio, carb_ratio, fat_ratio = 0.25, 0.45, 0.30
    
    protein_cals = calories * protein_ratio
    carb_cals = calories * carb_ratio
    fat_cals = calories * fat_ratio
    
    return {
        "protein": protein_cals / 4,  # 4 cal per gram
        "carbs": carb_cals / 4,
        "fats": fat_cals / 9  # 9 cal per gram
    }

def filter_foods_by_preferences(food_dict, diet_type, allergies, cuisine_pref):
    filtered_dict = {}
    
    for category, foods in food_dict.items():
        filtered_foods = {}
        for food, calories in foods.items():
            # Diet filtering
            if diet_type == "Vegetarian":
                non_veg_items = ["chicken", "beef", "salmon", "shrimp", "turkey", "smoked_salmon", "mutton", "fish"]
                if any(item in food.lower() for item in non_veg_items):
                    continue
            elif diet_type == "Vegan":
                non_vegan_items = ["chicken", "beef", "salmon", "shrimp", "turkey", "smoked_salmon", 
                                 "eggs", "milk", "cheese", "yogurt", "cottage_cheese", "greek_yogurt", 
                                 "paneer", "ghee", "mutton", "fish", "buttermilk", "lassi", "curd"]
                if any(item in food.lower() for item in non_vegan_items):
                    continue
            
            # Cuisine filtering
            if "Indian" in cuisine_pref:
                indian_foods = ["idli", "dosa", "paratha", "chapati", "dal", "paneer", "biryani", 
                              "curry", "sabzi", "roti", "naan", "sambar", "rasam", "chutney"]
                if not any(indian_food in food.lower() for indian_food in indian_foods):
                    # Allow general foods too
                    pass
            
            # Allergy filtering
            skip_food = False
            for allergy in allergies:
                if allergy == "Nuts" and ("nut" in food.lower() or "almond" in food.lower() or "walnut" in food.lower()):
                    skip_food = True
                elif allergy == "Dairy" and any(dairy in food.lower() for dairy in ["milk", "cheese", "yogurt", "paneer", "ghee", "butter"]):
                    skip_food = True
                elif allergy == "Gluten" and any(gluten in food.lower() for gluten in ["wheat", "bread", "pasta", "cereal", "naan", "roti"]):
                    skip_food = True
                elif allergy == "Eggs" and "egg" in food.lower():
                    skip_food = True
                elif allergy == "Shellfish" and "shrimp" in food.lower():
                    skip_food = True
                elif allergy == "Soy" and "tofu" in food.lower():
                    skip_food = True
            
            if not skip_food:
                filtered_foods[food] = calories
        
        if filtered_foods:
            filtered_dict[category] = filtered_foods
    
    return filtered_dict

def generate_grocery_list(weekly_meals):
    grocery_list = {}
    for day_meals in weekly_meals:
        for meal_type, items in day_meals.items():
            for item in items:
                if item in grocery_list:
                    grocery_list[item] += 1
                else:
                    grocery_list[item] = 1
    return grocery_list

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

def create_nutrition_chart(macros):
    labels = ['Protein', 'Carbs', 'Fats']
    values = [macros['protein'], macros['carbs'], macros['fats']]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))
    fig.update_layout(
        title_text="Daily Macro Distribution (grams)",
        annotations=[dict(text='Macros', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig

def create_weekly_progress_chart():
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    calories = [2100, 2050, 2200, 1950, 2150, 2300, 2000]
    target = [2000] * 7
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=calories, mode='lines+markers', name='Actual Calories', line=dict(color='#667eea')))
    fig.add_trace(go.Scatter(x=days, y=target, mode='lines', name='Target Calories', line=dict(color='#f093fb', dash='dash')))
    
    fig.update_layout(
        title='Weekly Calorie Tracking',
        xaxis_title='Day',
        yaxis_title='Calories',
        hovermode='x unified'
    )
    return fig

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'meal_history' not in st.session_state:
    st.session_state.meal_history = []
if 'favorite_meals' not in st.session_state:
    st.session_state.favorite_meals = []

# Main App Header
st.markdown("""
<div class="main-header">
    <h1>🧠 NutriAI - Smart Meal Planner</h1>
    <p>Revolutionary AI-powered meal planning for optimal nutrition and health</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    page = st.selectbox("Choose a feature:", [
        "🏠 Dashboard",
        "👤 Profile Setup",
        "🍽️ Meal Planner",
        "📊 Nutrition Analytics", 
        "💧 Hydration Tracker",
        "📅 Weekly Planner",
        "🛒 Smart Grocery List",
        "📈 Progress Tracking",
        "⭐ Favorite Meals",
        "🎯 Goal Setting",
        "🔬 Nutrition Calculator"
    ])
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    if 'current_meal_plan' in st.session_state:
        st.metric("Today's Calories", f"{sum(st.session_state.current_meal_plan.get('calories', [0]))}")
        st.metric("Meals Generated", len(st.session_state.meal_history))
        st.metric("Favorites", len(st.session_state.favorite_meals))

# Page Content
if page == "🏠 Dashboard":
    st.header("🏠 Welcome to Your Nutrition Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>10K+</h3>
            <p>Happy Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>50K+</h3>
            <p>Meals Generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>98%</h3>
            <p>Satisfaction Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>24/7</h3>
            <p>AI Support</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Generate Meal Plan", use_container_width=True):
            st.switch_page = "🍽️ Meal Planner"
    
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page = "📊 Nutrition Analytics"
    
    with col3:
        if st.button("👤 Update Profile", use_container_width=True):
            st.switch_page = "👤 Profile Setup"
    
    # Recent Activity
    st.markdown("### 📈 Recent Activity")
    if st.session_state.meal_history:
        for i, meal in enumerate(st.session_state.meal_history[-3:]):
            st.markdown(f"""
            <div class="feature-card">
                <strong>Meal Plan {i+1}</strong><br>
                Generated: {meal.get('date', 'Today')}<br>
                Calories: {meal.get('total_calories', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent meal plans. Generate your first meal plan to get started!")

elif page == "👤 Profile Setup":
    st.header("👤 Complete Your Profile")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Basic Information")
            name = st.text_input("Full Name", value=st.session_state.user_profile.get('name', ''))
            age = st.number_input("Age", min_value=1, max_value=120, value=st.session_state.user_profile.get('age', 25))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                index=["Male", "Female", "Other"].index(st.session_state.user_profile.get('gender', 'Male')))
            
            unit_preference = st.radio("Preferred units:", ["Metric (kg, cm)", "Imperial (lb, ft + in)"])
            
            if unit_preference == "Metric (kg, cm)":
                weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, 
                                       value=st.session_state.user_profile.get('weight', 70.0))
                height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0,
                                       value=st.session_state.user_profile.get('height', 170.0))
            else:
                weight_lb = st.number_input("Weight (lb)", min_value=1.0, max_value=600.0, value=154.0)
                height_ft = st.number_input("Height (ft)", min_value=1, max_value=8, value=5)
                height_in = st.number_input("Height (in)", min_value=0, max_value=11, value=7)
                
                weight = weight_lb / UNITS_KG_TO_LB
                height = (height_ft * 12 + height_in) * UNITS_IN_TO_CM
        
        with col2:
            st.subheader("Goals & Preferences")
            goal = st.selectbox("Primary Goal", [
                "Maintenance", "Weight Loss", "Weight Gain", "Muscle Gain"
            ], index=["Maintenance", "Weight Loss", "Weight Gain", "Muscle Gain"].index(
                st.session_state.user_profile.get('goal', 'Maintenance')))
            
            intensity = st.selectbox("Goal Intensity", ["conservative", "moderate", "aggressive"])
            
            activity_level = st.selectbox("Activity Level", [
                "Sedentary (office job)",
                "Lightly Active (light exercise 1-3 days/week)",
                "Moderately Active (moderate exercise 3-5 days/week)",
                "Very Active (hard exercise 6-7 days/week)",
                "Extremely Active (very hard exercise, physical job)"
            ])
            
            diet_type = st.selectbox("Diet Type", ["Non-Vegetarian", "Vegetarian", "Vegan"])
            
            cuisine_pref = st.multiselect("Cuisine Preferences", [
                "Indian", "Mediterranean", "Asian", "American", "Mexican", "Italian"
            ])
            
            allergies = st.multiselect("Food Allergies", [
                "Nuts", "Dairy", "Gluten", "Eggs", "Shellfish", "Soy"
            ])
            
            climate = st.selectbox("Climate", ["temperate", "hot", "cold"])
        
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)
        
        if submitted:
            st.session_state.user_profile = {
                'name': name,
                'age': age,
                'gender': gender,
                'weight': weight,
                'height': height,
                'goal': goal,
                'intensity': intensity,
                'activity_level': activity_level,
                'diet_type': diet_type,
                'cuisine_pref': cuisine_pref,
                'allergies': allergies,
                'climate': climate
            }
            st.success("✅ Profile saved successfully!")
            
            # Calculate and display metrics
            bmr = calculate_bmr(weight, height, age, gender)
            tdee = calculate_tdee(bmr, activity_level)
            target_calories = adjust_calories_for_goal(tdee, goal, intensity)
            bmi = calculate_bmi(weight, height)
            water_intake = calculate_water_intake(weight, activity_level, climate)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("BMR", f"{bmr:.0f} cal")
            with col2:
                st.metric("TDEE", f"{tdee:.0f} cal")
            with col3:
                st.metric("Target Calories", f"{target_calories:.0f} cal")
            with col4:
                st.metric("Daily Water", f"{water_intake:.1f}L")

elif page == "🍽️ Meal Planner":
    st.header("🍽️ AI-Powered Meal Planner")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please complete your profile first!")
        if st.button("Go to Profile Setup"):
            st.switch_page = "👤 Profile Setup"
    else:
        profile = st.session_state.user_profile
        
        # Calculate nutrition metrics
        bmr = calculate_bmr(profile['weight'], profile['height'], profile['age'], profile['gender'])
        tdee = calculate_tdee(bmr, profile['activity_level'])
        target_calories = adjust_calories_for_goal(tdee, profile['goal'], profile.get('intensity', 'moderate'))
        macros = calculate_macros(target_calories, profile['goal'])
        
        # Display current targets
        st.markdown("### 🎯 Your Daily Targets")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Calories", f"{target_calories:.0f}")
        with col2:
            st.metric("Protein", f"{macros['protein']:.0f}g")
        with col3:
            st.metric("Carbs", f"{macros['carbs']:.0f}g")
        with col4:
            st.metric("Fats", f"{macros['fats']:.0f}g")
        
        # Meal generation options
        st.markdown("### ⚙️ Meal Plan Options")
        col1, col2 = st.columns(2)
        
        with col1:
            meal_count = st.selectbox("Meals per day", [3, 4, 5, 6], index=1)
            include_snacks = st.checkbox("Include healthy snacks", value=True)
        
        with col2:
            meal_variety = st.selectbox("Variety Level", ["Low", "Medium", "High"], index=1)
            prep_time = st.selectbox("Max prep time per meal", ["15 min", "30 min", "45 min", "60+ min"])
        
        if st.button("🎯 Generate AI Meal Plan", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is creating your personalized meal plan..."):
                # Filter foods based on preferences
                filtered_breakfast = filter_foods_by_preferences(
                    food_items_breakfast, profile['diet_type'], 
                    profile['allergies'], profile['cuisine_pref']
                )
                filtered_lunch = filter_foods_by_preferences(
                    food_items_lunch, profile['diet_type'], 
                    profile['allergies'], profile['cuisine_pref']
                )
                filtered_dinner = filter_foods_by_preferences(
                    food_items_dinner, profile['diet_type'], 
                    profile['allergies'], profile['cuisine_pref']
                )
                
                if not filtered_breakfast or not filtered_lunch or not filtered_dinner:
                    st.error("⚠️ No suitable foods found with your dietary restrictions. Please adjust your preferences.")
                else:
                    # Calculate meal calories distribution
                    if meal_count == 3:
                        cal_dist = [0.3, 0.4, 0.3]
                    elif meal_count == 4:
                        cal_dist = [0.25, 0.35, 0.15, 0.25]  # breakfast, lunch, snack, dinner
                    elif meal_count == 5:
                        cal_dist = [0.2, 0.3, 0.1, 0.3, 0.1]
                    else:
                        cal_dist = [0.2, 0.25, 0.1, 0.25, 0.1, 0.1]
                    
                    meal_calories = [target_calories * dist for dist in cal_dist]
                    
                    # Generate meals
                    meal_items_morning, cal_m = knapsack(int(meal_calories[0]), filtered_breakfast)
                    meal_items_lunch, cal_l = knapsack(int(meal_calories[1]), filtered_lunch)
                    meal_items_dinner, cal_d = knapsack(int(meal_calories[2]), filtered_dinner)
                    
                    # Store meal plan
                    meal_plan = {
                        'breakfast': meal_items_morning,
                        'lunch': meal_items_lunch,
                        'dinner': meal_items_dinner,
                        'calories': [cal_m, cal_l, cal_d],
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'total_calories': cal_m + cal_l + cal_d
                    }
                    
                    st.session_state.current_meal_plan = meal_plan
                    st.session_state.meal_history.append(meal_plan)
                    
                    # Display meal plan
                    st.markdown("### 🍽️ Your Personalized Meal Plan")
                    
                    tab1, tab2, tab3 = st.tabs(["🌅 Breakfast", "☀️ Lunch", "🌙 Dinner"])
                    
                    with tab1:
                        st.markdown(f"**Target: {meal_calories[0]:.0f} calories**")
                        for item in meal_items_morning:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"• {item.replace('_', ' ').title()}")
                            with col2:
                                if st.button("⭐", key=f"fav_b_{item}"):
                                    st.session_state.favorite_meals.append(item)
                                    st.success("Added to favorites!")
                        st.success(f"**Total: {cal_m} calories**")
                    
                    with tab2:
                        st.markdown(f"**Target: {meal_calories[1]:.0f} calories**")
                        for item in meal_items_lunch:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"• {item.replace('_', ' ').title()}")
                            with col2:
                                if st.button("⭐", key=f"fav_l_{item}"):
                                    st.session_state.favorite_meals.append(item)
                                    st.success("Added to favorites!")
                        st.success(f"**Total: {cal_l} calories**")
                    
                    with tab3:
                        st.markdown(f"**Target: {meal_calories[2]:.0f} calories**")
                        for item in meal_items_dinner:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"• {item.replace('_', ' ').title()}")
                            with col2:
                                if st.button("⭐", key=f"fav_d_{item}"):
                                    st.session_state.favorite_meals.append(item)
                                    st.success("Added to favorites!")
                        st.success(f"**Total: {cal_d} calories**")
                    
                    total_planned = cal_m + cal_l + cal_d
                    accuracy = (total_planned / target_calories) * 100
                    
                    if accuracy >= 95:
                        st.markdown(f"""
                        <div class="success-card">
                            <h4>🎯 Excellent Match!</h4>
                            <p>Total: {total_planned} / {target_calories:.0f} calories ({accuracy:.1f}% accuracy)</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="warning-card">
                            <h4>⚠️ Good Match</h4>
                            <p>Total: {total_planned} / {target_calories:.0f} calories ({accuracy:.1f}% accuracy)</p>
                        </div>
                        """, unsafe_allow_html=True)

elif page == "📊 Nutrition Analytics":
    st.header("📊 Nutrition Analytics Dashboard")
    
    if st.session_state.user_profile and 'current_meal_plan' in st.session_state:
        profile = st.session_state.user_profile
        target_calories = adjust_calories_for_goal(
            calculate_tdee(
                calculate_bmr(profile['weight'], profile['height'], profile['age'], profile['gender']),
                profile['activity_level']
            ),
            profile['goal'],
            profile.get('intensity', 'moderate')
        )
        
        macros = calculate_macros(target_calories, profile['goal'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Macro distribution chart
            fig = create_nutrition_chart(macros)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Weekly progress chart
            fig2 = create_weekly_progress_chart()
            st.plotly_chart(fig2, use_container_width=True)
        
        # Nutrition insights
        st.markdown("### 🔍 Nutrition Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>💪 Protein Focus</h4>
                <p>Your protein target supports your muscle gain goals. Consider spreading intake across all meals.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>🌾 Carb Timing</h4>
                <p>Optimize carb intake around workouts for better performance and recovery.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>🥑 Healthy Fats</h4>
                <p>Include omega-3 rich foods like salmon and walnuts for optimal health.</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("Complete your profile and generate a meal plan to view analytics.")

elif page == "💧 Hydration Tracker":
    st.header("💧 Smart Hydration Tracker")
    
    if st.session_state.user_profile:
        profile = st.session_state.user_profile
        recommended_water = calculate_water_intake(
            profile['weight'], 
            profile['activity_level'], 
            profile.get('climate', 'temperate')
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Daily Water Goal", f"{recommended_water:.1f}L")
            st.metric("In Glasses (250ml)", f"{recommended_water*4:.0f} glasses")
            
            # Water intake tracker
            if 'water_intake_today' not in st.session_state:
                st.session_state.water_intake_today = 0
            
            glasses_drunk = st.number_input("Glasses consumed today", 
                                          min_value=0, max_value=20, 
                                          value=st.session_state.water_intake_today)
            
            if st.button("💧 Update Water Intake"):
                st.session_state.water_intake_today = glasses_drunk
                liters_consumed = glasses_drunk * 0.25
                percentage = (liters_consumed / recommended_water) * 100
                
                if percentage >= 100:
                    st.success(f"🎉 Great job! You've reached {percentage:.0f}% of your daily goal!")
                elif percentage >= 75:
                    st.info(f"👍 Good progress! You're at {percentage:.0f}% of your daily goal.")
                else:
                    st.warning(f"💪 Keep going! You're at {percentage:.0f}% of your daily goal.")
        
        with col2:
            # Hydration tips
            st.markdown("### 💡 Hydration Tips")
            tips = [
                "🌅 Start your day with a glass of water",
                "🍽️ Drink water before each meal",
                "⏰ Set hourly water reminders",
                "🍋 Add lemon or cucumber for flavor",
                "🏃‍♂️ Increase intake during exercise",
                "🌡️ Drink more in hot weather"
            ]
            
            for tip in tips:
                st.markdown(f"• {tip}")
    
    else:
        st.info("Complete your profile to get personalized hydration recommendations.")

elif page == "📅 Weekly Planner":
    st.header("📅 7-Day Smart Meal Planner")
    
    if 'current_meal_plan' in st.session_state:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🗓️ Generate 7-Day Plan", type="primary"):
                weekly_plan = []
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                
                base_plan = st.session_state.current_meal_plan
                
                for i, day in enumerate(days):
                    # Create variation for each day
                    daily_plan = {
                        'breakfast': random.sample(base_plan['breakfast'], 
                                                 min(3, len(base_plan['breakfast']))),
                        'lunch': random.sample(base_plan['lunch'], 
                                             min(3, len(base_plan['lunch']))),
                        'dinner': random.sample(base_plan['dinner'], 
                                              min(3, len(base_plan['dinner'])))
                    }
                    weekly_plan.append(daily_plan)
                
                st.session_state.weekly_plan = weekly_plan
        
        with col2:
            meal_prep_day = st.selectbox("Meal prep day", 
                                       ["Sunday", "Monday", "Tuesday", "Wednesday", 
                                        "Thursday", "Friday", "Saturday"])
            
            if st.button("📋 Generate Prep Schedule"):
                st.info(f"🍳 Meal prep scheduled for {meal_prep_day}")
        
        # Display weekly plan
        if 'weekly_plan' in st.session_state:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            for i, day in enumerate(days):
                with st.expander(f"📅 {day}", expanded=(i == 0)):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**🌅 Breakfast**")
                        for item in st.session_state.weekly_plan[i]['breakfast']:
                            st.write(f"• {item.replace('_', ' ').title()}")
                    
                    with col2:
                        st.markdown("**☀️ Lunch**")
                        for item in st.session_state.weekly_plan[i]['lunch']:
                            st.write(f"• {item.replace('_', ' ').title()}")
                    
                    with col3:
                        st.markdown("**🌙 Dinner**")
                        for item in st.session_state.weekly_plan[i]['dinner']:
                            st.write(f"• {item.replace('_', ' ').title()}")
    
    else:
        st.info("Generate a daily meal plan first to create your weekly schedule.")

elif page == "🛒 Smart Grocery List":
    st.header("🛒 AI-Generated Grocery List")
    
    if 'weekly_plan' in st.session_state:
        grocery_list = generate_grocery_list(st.session_state.weekly_plan)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Organize by categories
            categories = {
                '🥩 Proteins': ['chicken', 'beef', 'salmon', 'tofu', 'eggs', 'shrimp', 'paneer'],
                '🌾 Grains & Starches': ['rice', 'quinoa', 'bread', 'pasta', 'oatmeal', 'roti', 'naan'],
                '🥬 Vegetables': ['broccoli', 'spinach', 'carrots', 'tomatoes', 'peppers', 'onions'],
                '🍎 Fruits': ['bananas', 'apples', 'berries', 'oranges', 'mango', 'papaya'],
                '🥛 Dairy': ['milk', 'yogurt', 'cheese', 'paneer', 'ghee'],
                '🥜 Nuts & Seeds': ['almonds', 'walnuts', 'chia', 'flax'],
                '🧂 Others': []
            }
            
            categorized_list = {cat: [] for cat in categories.keys()}
            
            for item, count in grocery_list.items():
                categorized = False
                for category, keywords in categories.items():
                    if any(keyword in item.lower() for keyword in keywords):
                        categorized_list[category].append(f"{item.replace('_', ' ').title()} (×{count})")
                        categorized = True
                        break
                if not categorized:
                    categorized_list['🧂 Others'].append(f"{item.replace('_', ' ').title()} (×{count})")
            
            for category, items in categorized_list.items():
                if items:
                    st.markdown(f"### {category}")
                    for item in items:
                        col_item, col_check = st.columns([4, 1])
                        with col_item:
                            st.write(f"• {item}")
                        with col_check:
                            st.checkbox("✓", key=f"check_{item}")
        
        with col2:
            st.markdown("### 📊 Shopping Stats")
            total_items = len(grocery_list)
            estimated_cost = total_items * 3.5  # Rough estimate
            
            st.metric("Total Items", total_items)
            st.metric("Estimated Cost", f"${estimated_cost:.0f}")
            st.metric("Shopping Time", f"{total_items//10 + 1} hours")
            
            # Download options
            grocery_text = "🛒 WEEKLY GROCERY LIST\n" + "="*30 + "\n\n"
            for category, items in categorized_list.items():
                if items:
                    grocery_text += f"{category}\n"
                    for item in items:
                        grocery_text += f"☐ {item}\n"
                    grocery_text += "\n"
            
            st.download_button(
                label="📥 Download List",
                data=grocery_text,
                file_name=f"grocery_list_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            if st.button("📱 Send to Phone", use_container_width=True):
                st.info("📲 Feature coming soon!")
    
    else:
        st.info("Generate a weekly meal plan first to create your grocery list.")

elif page == "📈 Progress Tracking":
    st.header("📈 Progress Tracking & Analytics")
    
    # Simulated progress data
    dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
    weight_data = [70 + random.uniform(-0.5, 0.5) + (i * -0.05) for i in range(len(dates))]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weight tracking chart
        fig = px.line(x=dates, y=weight_data, title="Weight Progress")
        fig.update_layout(xaxis_title="Date", yaxis_title="Weight (kg)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Progress metrics
        st.markdown("### 📊 Progress Summary")
        st.metric("Weight Change", "-1.5 kg", delta="-1.5")
        st.metric("Avg Daily Calories", "2,050", delta="50")
        st.metric("Workout Days", "20/30", delta="5")
        st.metric("Water Goal Met", "85%", delta="10%")
    
    # Achievement badges
    st.markdown("### 🏆 Achievements")
    achievements = [
        {"name": "First Week", "icon": "🎯", "desc": "Completed your first week"},
        {"name": "Hydration Hero", "icon": "💧", "desc": "Met water goals 7 days straight"},
        {"name": "Meal Prep Master", "icon": "🍱", "desc": "Prepared meals for entire week"},
        {"name": "Goal Crusher", "icon": "💪", "desc": "Achieved monthly weight goal"}
    ]
    
    cols = st.columns(4)
    for i, achievement in enumerate(achievements):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card" style="text-align: center;">
                <div style="font-size: 2rem;">{achievement['icon']}</div>
                <h4>{achievement['name']}</h4>
                <p>{achievement['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "⭐ Favorite Meals":
    st.header("⭐ Your Favorite Meals")
    
    if st.session_state.favorite_meals:
        st.markdown(f"### You have {len(st.session_state.favorite_meals)} favorite meals")
        
        for i, meal in enumerate(st.session_state.favorite_meals):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"• {meal.replace('_', ' ').title()}")
            
            with col2:
                if st.button("🍽️ Add to Plan", key=f"add_{i}"):
                    st.success("Added to current meal plan!")
            
            with col3:
                if st.button("🗑️ Remove", key=f"remove_{i}"):
                    st.session_state.favorite_meals.remove(meal)
                    st.rerun()
        
        if st.button("📋 Create Plan from Favorites"):
            st.info("Creating meal plan from your favorite foods...")
    
    else:
        st.info("No favorite meals yet. Add meals to favorites from the meal planner!")

elif page == "🎯 Goal Setting":
    st.header("🎯 Advanced Goal Setting")
    
    with st.form("goal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Primary Goals")
            primary_goal = st.selectbox("Main Objective", [
                "Weight Loss", "Weight Gain", "Muscle Gain", "Maintenance",
                "Athletic Performance", "General Health"
            ])
            
            target_weight = st.number_input("Target Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
            target_date = st.date_input("Target Date", value=datetime.now() + timedelta(days=90))
            
            weekly_goal = st.selectbox("Weekly Progress", [
                "0.25 kg/week", "0.5 kg/week", "0.75 kg/week", "1.0 kg/week"
            ])
        
        with col2:
            st.subheader("Lifestyle Factors")
            workout_days = st.slider("Workout days per week", 0, 7, 3)
            sleep_hours = st.slider("Average sleep hours", 4, 12, 8)
            stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
            
            health_conditions = st.multiselect("Health Conditions", [
                "Diabetes", "Hypertension", "Heart Disease", "PCOS", "Thyroid"
            ])
        
        if st.form_submit_button("🎯 Set Goals", use_container_width=True):
            st.success("Goals updated successfully!")
            
            # Calculate timeline
            current_weight = st.session_state.user_profile.get('weight', 70)
            weight_diff = abs(target_weight - current_weight)
            weeks_needed = weight_diff / float(weekly_goal.split()[0])
            
            st.info(f"📅 Estimated timeline: {weeks_needed:.0f} weeks to reach your goal")

elif page == "🔬 Nutrition Calculator":
    st.header("🔬 Advanced Nutrition Calculator")
    
    tab1, tab2, tab3 = st.tabs(["🧮 Calorie Calculator", "🥗 Macro Calculator", "💊 Supplement Guide"])
    
    with tab1:
        st.subheader("Precision Calorie Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            calc_weight = st.number_input("Weight (kg)", value=70.0)
            calc_height = st.number_input("Height (cm)", value=170.0)
            calc_age = st.number_input("Age", value=30)
            calc_gender = st.selectbox("Gender", ["Male", "Female"])
        
        with col2:
            calc_activity = st.selectbox("Activity Level", [
                "Sedentary", "Lightly Active", "Moderately Active", 
                "Very Active", "Extremely Active"
            ])
            calc_goal = st.selectbox("Goal", ["Maintenance", "Weight Loss", "Weight Gain", "Muscle Gain"])
        
        if st.button("🧮 Calculate"):
            bmr = calculate_bmr(calc_weight, calc_height, calc_age, calc_gender)
            tdee = calculate_tdee(bmr, calc_activity)
            target = adjust_calories_for_goal(tdee, calc_goal)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("BMR", f"{bmr:.0f} cal")
            with col2:
                st.metric("TDEE", f"{tdee:.0f} cal")
            with col3:
                st.metric("Target", f"{target:.0f} cal")
    
    with tab2:
        st.subheader("Macro Distribution Calculator")
        
        calories_input = st.number_input("Daily Calories", value=2000)
        goal_input = st.selectbox("Goal Type", ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintenance"])
        
        if st.button("Calculate Macros"):
            macros = calculate_macros(calories_input, goal_input)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Protein", f"{macros['protein']:.0f}g")
            with col2:
                st.metric("Carbs", f"{macros['carbs']:.0f}g")
            with col3:
                st.metric("Fats", f"{macros['fats']:.0f}g")
            
            # Macro chart
            fig = create_nutrition_chart(macros)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Personalized Supplement Guide")
        
        supplements = {
            "Weight Loss": ["Green Tea Extract", "L-Carnitine", "CLA", "Chromium"],
            "Muscle Gain": ["Whey Protein", "Creatine", "BCAA", "Beta-Alanine"],
            "General Health": ["Multivitamin", "Omega-3", "Vitamin D", "Probiotics"],
            "Athletic Performance": ["Pre-workout", "Electrolytes", "Recovery Formula"]
        }
        
        goal_supp = st.selectbox("Select Goal", list(supplements.keys()))
        
        st.markdown(f"### Recommended for {goal_supp}:")
        for supp in supplements[goal_supp]:
            st.markdown(f"• **{supp}** - Consult with healthcare provider")
        
        st.warning("⚠️ Always consult with a healthcare professional before starting any supplement regimen.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h3>🧠 NutriAI - Your AI Nutrition Companion</h3>
    <p>Revolutionizing nutrition with artificial intelligence • Built with ❤️ using Streamlit</p>
    <p>© 2024 NutriAI. Transform your health with smart meal planning.</p>
</div>
""", unsafe_allow_html=True)

# Custom CSS for animations and modern styling
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)