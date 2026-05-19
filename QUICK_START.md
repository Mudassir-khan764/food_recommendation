# 🚀 Quick Start Guide - Food Tracking System

## ✅ System Status: FULLY OPERATIONAL

All components have been successfully validated and are ready to use!

---

## 📍 What's Ready

✅ MongoDB food database with 40+ items  
✅ Flask API endpoints for food tracking  
✅ HTML templates for tracking dashboard and profile  
✅ Real-time AJAX functionality  
✅ User authentication system  
✅ Nutritional goal management  

---

## 🏃 Quick Start (5 Minutes)

### Step 1: Start the Flask Server
```bash
cd c:\Users\CSC\Desktop\clone\AI-Meal-Planner
python app.py
```

You should see:
```
⚠️ YOLOv5 not available - using heuristic food detection
🚀 Initializing Food Object Detection System...
✅ System initialized successfully!
* Running on http://127.0.0.1:5000
```

### Step 2: Open in Browser
Go to: **http://127.0.0.1:5000**

### Step 3: Create Account
1. Click **Sign Up**
2. Enter email, name, password
3. Click **Register**

### Step 4: Start Tracking!
1. Click **"Track Food"** in navigation
2. Select meal type (Breakfast/Lunch/Snack/Dinner)
3. Search for food (e.g., "eggs", "chicken", "rice")
4. Enter quantity (default 100g)
5. Click **"Add Food"**
6. Watch the totals update in real-time! 🎯

### Step 5: View Your Profile
1. Click **"Profile"** in navigation
2. See your daily totals vs. goals
3. View circular progress charts
4. Edit your daily nutritional goals if desired

---

## 📊 Available Foods (40+ Items)

### Breakfast 🌅
eggs, oatmeal, toast, milk, yogurt, banana, apple, orange

### Indian 🍛
biryani, samosa, dosa, naan, chapati, dal, curry, gulab_jamun

### Vegetables 🥦
spinach, broccoli, carrot, tomato, cucumber, lettuce

### Main Dishes 🍽️
pizza, burger, sandwich, pasta, rice, chicken, fish, beef

### Snacks 🥜
almonds, peanuts, peanut_butter, cheese, ice_cream, donut, chocolate, protein_bar, granola

---

## 🎯 Key Features

| Feature | Description |
|---------|------------|
| **Real-time Updates** | No page refresh needed - instant meal totals |
| **Auto-complete Search** | Type food name and get suggestions |
| **Meal Organization** | Foods grouped by meal type |
| **Nutritional Tracking** | Calories, Protein, Carbs, Fat |
| **Goal Management** | Set and track daily nutritional targets |
| **Progress Charts** | Visual circular progress indicators |
| **Remove Items** | Delete foods from meals instantly |
| **Daily Summary** | Aggregate all meals for the day |

---

## 💡 Examples

### Example 1: Add breakfast
1. Meal Type: **Breakfast**
2. Food: **eggs**
3. Quantity: **200** g
4. ➜ Adds 310 kcal to breakfast

### Example 2: Add lunch
1. Meal Type: **Lunch**
2. Food: **chicken**
3. Quantity: **150** g
4. ➜ Adds 247.5 kcal to lunch

### Example 3: View profile
1. Click **Profile**
2. See today's totals (e.g., 2150 kcal, 95g protein)
3. Compare with goals (2000 kcal default)
4. See circular progress: 107% of calorie goal ✓

---

## 🔍 Common Tasks

### How to search for a specific food?
- In the **"Track Food"** page, type in the food name field
- Minimum 2 characters to trigger search
- Select from dropdown suggestions

### How to change daily goals?
- Go to **"Profile"** page
- Scroll to **"Daily Nutritional Goals"**
- Update Calories, Protein, Carbs, Fat values
- Click **"Save Goals"**

### How to track a meal?
- Go to **"Track Food"** page
- Select meal type (Breakfast/Lunch/Snack/Dinner)
- Add foods to that meal
- All meals auto-aggregate into daily total

### How to remove a food?
- Go to **"Track Food"** page
- Find the food item you added
- Click trash/remove button
- Totals update instantly

---

## 📈 Expected Workflow

```
Sign Up
  ↓
Login
  ↓
Go to Track Page
  ↓
Add Breakfast Foods (e.g., eggs + toast)
  ↓
Add Lunch Foods (e.g., chicken + rice)
  ↓
View Today's Summary (totals + goals)
  ↓
Check Profile for Progress Charts
  ↓
Adjust Daily Goals if Needed
```

---

## ⚙️ Technical Details

**Database:** MongoDB (40+ foods pre-loaded)  
**Backend:** Flask (Python)  
**Frontend:** HTML5, CSS3, JavaScript  
**API:** RESTful JSON endpoints  
**Auth:** bcrypt password hashing  

---

## 🆘 Troubleshooting

### Flask won't start
```bash
# Check Python is installed
python --version

# Check MongoDB is running (should show connection success)
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017/').admin.command('ping')"
```

### Foods don't show in search
```bash
# Re-populate food database
python populate_foods.py
```

### Can't login
- Make sure you signed up first
- Check email and password are correct
- MongoDB must be running

### Page not loading
- Check Flask server is running
- Check http://127.0.0.1:5000 URL is correct
- Try http://localhost:5000 instead
- Clear browser cache (Ctrl+Shift+Delete)

---

## 📱 Responsive Design

Works on:
- ✅ Desktop browsers (Chrome, Firefox, Edge)
- ✅ Tablets (iPad, Android)
- ✅ Mobile phones

Food cards automatically stack for smaller screens.

---

## 🎓 Learn More

For detailed implementation info, see: **FOOD_TRACKING_IMPLEMENTATION.md**

For API documentation, see code comments in: **app.py** and **database.py**

---

## ✨ Pro Tips

1. **Bulk Add:** Add common meals at once (e.g., breakfast = oatmeal + banana + milk)
2. **Default Values:** Most foods use 100g as default - adjust as needed
3. **Portion Types:** Switch between g (grams), ml (milliliters), piece, or cup
4. **Daily Check-in:** Set a reminder to log meals daily for best results
5. **Goal Tuning:** Adjust goals based on your fitness plan

---

## 🎉 You're Ready!

Start the server, sign up, and begin tracking your meals!

```bash
python app.py
# Then visit: http://127.0.0.1:5000
```

**Happy tracking! 🥗📊**
