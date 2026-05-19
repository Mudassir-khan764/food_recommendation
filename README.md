<<<<<<< HEAD
# 🧠 NutriAI - Smart Meal Planner

An AI-powered meal planning application that creates personalized nutrition plans based on your health profile, dietary preferences, and fitness goals.

## ✨ Features

### 🎯 Personalized Planning
- **BMR & TDEE Calculations**: Scientific formulas for accurate calorie needs
- **BMI Assessment**: Body Mass Index calculation with health categories
- **Goal-Oriented**: Weight loss, muscle gain, or maintenance plans
- **Macro Distribution**: Personalized protein, carbs, and fat ratios

### 🍽️ Advanced Dietary Support
- **Multiple Diet Types**: Vegetarian, Vegan, Keto, Paleo, and more
- **Allergy Management**: Comprehensive allergy filtering system
- **Cuisine Preferences**: Indian, Continental, Chinese options
- **Budget Considerations**: Low, medium, high budget meal options

### 🏥 Health Integration
- **Medical Conditions**: Diabetes, hypertension, thyroid support
- **Activity Levels**: From sedentary to athlete-level planning
- **Hydration Tracking**: Personalized water intake recommendations
- **Sleep & Lifestyle**: Holistic health approach

### 🤖 Smart Technology
- **Knapsack Algorithm**: Optimal meal combination selection
- **Real-time Validation**: Form validation with instant feedback
- **Responsive Design**: Modern UI that works on all devices
- **Interactive Dashboard**: Dynamic meal plan visualization

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Meal-Planner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

## 📱 How to Use

### Step 1: Personal Profile
- Enter your age, gender, height, and weight
- Add body fat percentage (optional)
- Select your activity level

### Step 2: Health & Lifestyle
- Choose your activity level (sedentary to athlete)
- Specify any medical conditions
- Set water intake and sleep duration preferences

### Step 3: Dietary Preferences
- Select your diet type (vegetarian, vegan, keto, etc.)
- Choose cuisine preferences
- Set budget and cooking time constraints
- Mark any food allergies

### Step 4: Fitness Goals
- Define your primary goal (weight loss, muscle gain, maintenance)
- Set target weight (optional)
- Specify workout frequency
- Choose protein preference level

### Step 5: Generate Plan
- Click "Generate My Advanced Meal Plan"
- View your personalized nutrition dashboard
- Download or regenerate as needed

## 🏗️ Project Structure

```
AI-Meal-Planner/
├── app.py                 # Main Flask application
├── run.py                 # Application startup script
├── data.py                # Food database
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Landing page
│   ├── dashboard.html    # Main application interface
│   ├── login.html        # Login page
│   └── signup.html       # Registration page
├── static/
│   ├── css/
│   │   └── style.css     # Modern styling
│   └── js/
│       └── dashboard.js  # Interactive functionality
└── README.md             # This file
```

## 🧮 Algorithms & Calculations

### BMR (Basal Metabolic Rate)
Uses the Mifflin-St Jeor Equation:
- **Men**: BMR = 9.99 × weight(kg) + 6.25 × height(cm) - 4.92 × age + 5
- **Women**: BMR = 9.99 × weight(kg) + 6.25 × height(cm) - 4.92 × age - 161

### TDEE (Total Daily Energy Expenditure)
BMR multiplied by activity factor:
- Sedentary: 1.2
- Light Activity: 1.375
- Moderate Activity: 1.55
- Active: 1.725
- Athlete: 1.9

### Meal Optimization
Uses a knapsack algorithm to select optimal food combinations that:
- Meet calorie targets
- Respect dietary restrictions
- Consider allergies and preferences
- Maximize nutritional value

## 🎨 Design Features

### Modern UI/UX
- **Gradient Backgrounds**: Beautiful visual appeal
- **Smooth Animations**: Enhanced user experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Real-time form validation

### Color Scheme
- Primary: Indigo (#6366f1)
- Secondary: Cyan (#06b6d4)
- Accent: Amber (#f59e0b)
- Success: Emerald (#10b981)

## 🔧 Technical Stack

### Backend
- **Flask**: Python web framework
- **Python**: Core programming language
- **JSON**: Data exchange format

### Frontend
- **HTML5**: Modern markup
- **CSS3**: Advanced styling with custom properties
- **JavaScript**: Interactive functionality
- **Bootstrap 5**: Responsive framework
- **Font Awesome**: Icon library

### Algorithms
- **Knapsack Algorithm**: Meal optimization
- **Mifflin-St Jeor**: BMR calculation
- **Custom Macros**: Nutrient distribution

## 📊 Food Database

The application includes comprehensive food databases:

### Breakfast Items
- Proteins: Eggs, Greek yogurt, cottage cheese
- Grains: Oatmeal, whole wheat bread, quinoa
- Fruits: Berries, bananas, apples
- Healthy fats: Nuts, seeds, avocado

### Lunch & Dinner
- Lean proteins: Chicken, fish, legumes
- Complex carbs: Rice, pasta, potatoes
- Vegetables: Leafy greens, colorful vegetables
- Healthy fats: Olive oil, nuts, seeds

### Snacks
- Protein bars, mixed nuts, Greek yogurt
- Fruits with nut butter
- Vegetable sticks with hummus

## 🚀 Future Enhancements

- [ ] AI-powered recipe suggestions
- [ ] Grocery list generation
- [ ] Meal prep scheduling
- [ ] Progress tracking
- [ ] Social sharing features
- [ ] Mobile app development
- [ ] Integration with fitness trackers
- [ ] Nutritionist consultation booking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Mifflin-St Jeor equation for BMR calculations
- Bootstrap team for the responsive framework
- Font Awesome for beautiful icons
- Flask community for the excellent web framework

## 📞 Support

For support, email support@nutriai.com or create an issue in the repository.

---

**Made with ❤️ for better health and nutrition**
=======
# food_recommendation
>>>>>>> 5a36165bbe9ca05f0ba9db9400a656b03161100e
