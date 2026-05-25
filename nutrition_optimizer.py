
import json
import os
from typing import Dict, List, Tuple, Optional
from indian_food_database import INDIAN_FOOD_DATABASE, NUTRIENT_REQUIREMENTS

class NutritionOptimizer:
    """
    AI Nutrition Optimization Engine for Indian users.
    Generates cost-effective weekly grocery plans that meet nutritional requirements.
    """

    def __init__(self):
        self.food_db = INDIAN_FOOD_DATABASE
        self.nutrient_reqs = NUTRIENT_REQUIREMENTS

    def calculate_age_adjusted_targets(self, daily_calories: int, goal: str, weight: float, age: int) -> Dict:
        """Calculate weekly nutritional targets adjusted for age"""
        # Age-based calorie adjustment
        age_factor = self.get_age_calorie_factor(age)
        adjusted_daily_calories = daily_calories * age_factor
        weekly_calories = adjusted_daily_calories * 7

        # Protein requirements based on goal and age
        if goal.lower() == "weight loss":
            daily_protein = weight * 1.2  # g per kg
        elif goal.lower() == "muscle gain":
            daily_protein = weight * 1.6  # g per kg
        else:  # maintenance
            daily_protein = weight * 1.0  # g per kg

        # Age-based protein adjustment (10% increase for age > 50)
        if age > 50:
            daily_protein *= 1.1

        weekly_protein = daily_protein * 7

        return {
            "weekly_calories": weekly_calories,
            "weekly_protein": weekly_protein,
            "daily_protein": daily_protein,
            "daily_calories": adjusted_daily_calories,
            "age_factor": age_factor
        }

    def get_age_calorie_factor(self, age: int) -> float:
        """Get calorie adjustment factor based on age group"""
        if age <= 30:
            return 1.0  # Normal metabolism (18-30)
        elif age <= 50:
            return 0.95  # Slightly reduced (30-50)
        else:
            return 0.9  # Reduced calories (50+)

    def calculate_targets(self, daily_calories: int, goal: str, weight: float, age: int = None) -> Dict:
        """Calculate weekly nutritional targets (backward compatibility)"""
        if age is not None:
            return self.calculate_age_adjusted_targets(daily_calories, goal, weight, age)
        else:
            # Fallback to original logic if age not provided
            weekly_calories = daily_calories * 7

            # Protein requirements based on goal
            if goal.lower() == "weight loss":
                daily_protein = weight * 1.2  # g per kg
            elif goal.lower() == "muscle gain":
                daily_protein = weight * 1.6  # g per kg
            else:  # maintenance
                daily_protein = weight * 1.0  # g per kg

            weekly_protein = daily_protein * 7

            return {
                "weekly_calories": weekly_calories,
                "weekly_protein": weekly_protein,
                "daily_protein": daily_protein
            }

    def filter_foods_by_preference(self, diet_preference: str) -> Dict:
        """Filter foods based on vegetarian/non-vegetarian preference"""
        if diet_preference.lower() == "veg":
            return {k: v for k, v in self.food_db.items() if v["veg"]}
        elif diet_preference.lower() == "non-veg":
            return self.food_db  # Include all foods
        else:
            return {k: v for k, v in self.food_db.items() if v["veg"]}  # Default to veg

    def rank_foods_by_efficiency(self, foods: Dict, priority_nutrient: Optional[str] = None) -> List[Tuple[str, float]]:
        """Rank foods by nutritional efficiency (nutrient per rupee)"""
        rankings = []

        for food_name, food_data in foods.items():
            price = food_data["price_per_100g"]

            if price == 0:
                continue

            # Calculate efficiency scores
            protein_efficiency = food_data["protein"] / price
            calorie_efficiency = food_data["calories"] / price

            # Priority nutrient efficiency
            priority_efficiency = 0
            if priority_nutrient and priority_nutrient in food_data:
                priority_efficiency = food_data[priority_nutrient] / price

            # Combined score (weighted)
            if priority_nutrient:
                combined_score = (protein_efficiency * 0.4 +
                                calorie_efficiency * 0.3 +
                                priority_efficiency * 0.3)
            else:
                combined_score = (protein_efficiency * 0.6 + calorie_efficiency * 0.4)

            rankings.append((food_name, combined_score))

        # Sort by efficiency score (highest first)
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings

    def optimize_grocery_plan(self, daily_calories: int, weekly_budget: float,
                            goal: str, weight: float, deficiencies: List[str],
                            diet_preference: str, age: int = None) -> Dict:
        """
        Generate optimized weekly grocery plan using constraint-based optimization
        """

        # Calculate targets
        targets = self.calculate_targets(daily_calories, goal, weight, age)

        # Filter foods by preference
        available_foods = self.filter_foods_by_preference(diet_preference)

        # Initialize plan
        plan = {
            "groceries": {},
            "total_cost": 0,
            "total_calories": 0,
            "total_protein": 0,
            "total_iron": 0,
            "total_vitamin_b12": 0,
            "budget_remaining": weekly_budget,
            "weekly_budget": weekly_budget,  # Store original budget
            "targets": targets,
            "deficiencies_fixed": False
        }

        # Define food categories and their allocation percentages
        categories = {
            "cereals": ["rice", "wheat_flour", "poha", "oats"],
            "pulses": ["moong_dal", "chana_dal", "chickpeas", "soy_chunks"],
            "proteins": ["eggs", "chicken", "paneer", "fish"],
            "dairy": ["milk", "curd", "cheese"],
            "vegetables": ["onions", "tomatoes", "spinach", "carrots", "cabbage", "potatoes"],
            "fruits": ["bananas", "oranges", "apples"]
        }

        # Budget allocation per category
        budget_allocation = {
            "cereals": 0.25,  # 25% for staples
            "pulses": 0.20,   # 20% for protein-rich legumes
            "proteins": 0.20, # 20% for animal proteins
            "dairy": 0.15,    # 15% for dairy
            "vegetables": 0.15, # 15% for vegetables
            "fruits": 0.05    # 5% for fruits
        }

        # Nutritional targets per category (approximate weekly portions)
        nutritional_targets = {
            "cereals": {"calories": targets["weekly_calories"] * 0.4, "protein": targets["weekly_protein"] * 0.2},
            "pulses": {"calories": targets["weekly_calories"] * 0.15, "protein": targets["weekly_protein"] * 0.3},
            "proteins": {"calories": targets["weekly_calories"] * 0.15, "protein": targets["weekly_protein"] * 0.25},
            "dairy": {"calories": targets["weekly_calories"] * 0.1, "protein": targets["weekly_protein"] * 0.1},
            "vegetables": {"calories": targets["weekly_calories"] * 0.1, "protein": targets["weekly_protein"] * 0.1},
            "fruits": {"calories": targets["weekly_calories"] * 0.1, "protein": targets["weekly_protein"] * 0.05}
        }

        # Process each category
        for category, foods in categories.items():
            category_budget = weekly_budget * budget_allocation[category]
            category_calorie_target = nutritional_targets[category]["calories"]
            category_protein_target = nutritional_targets[category]["protein"]

            available_category_foods = [f for f in foods if f in available_foods]

            if not available_category_foods:
                continue

            # Sort foods by nutritional efficiency
            if category == "vegetables" and "iron" in deficiencies:
                # Prioritize iron-rich vegetables for iron deficiency
                sorted_foods = sorted(available_category_foods,
                                    key=lambda f: available_foods[f]["iron"] / available_foods[f]["price_per_100g"],
                                    reverse=True)
            elif category == "dairy" and ("vitamin_b12" in deficiencies or "b12" in deficiencies):
                # Prioritize B12-rich dairy for B12 deficiency
                sorted_foods = sorted(available_category_foods,
                                    key=lambda f: available_foods[f]["vitamin_b12"] / available_foods[f]["price_per_100g"],
                                    reverse=True)
            else:
                # Default: sort by calorie efficiency
                sorted_foods = sorted(available_category_foods,
                                    key=lambda f: (available_foods[f]["calories"] / available_foods[f]["price_per_100g"]),
                                    reverse=True)

            # Distribute budget across foods in the category
            foods_in_category = min(len(sorted_foods), 3)  # Use up to 3 foods per category
            budget_per_food = category_budget / foods_in_category

            for food in sorted_foods[:foods_in_category]:
                food_data = available_foods[food]

                # Calculate how much to buy based on nutritional targets and budget
                # Prioritize meeting calorie and protein targets
                calorie_density = food_data["calories"] / food_data["price_per_100g"]
                protein_density = food_data["protein"] / food_data["price_per_100g"]

                # Estimate quantity needed
                if category in ["cereals", "pulses"]:
                    # For calorie-dense foods, calculate based on calorie target
                    calories_needed = category_calorie_target / foods_in_category
                    quantity_for_calories = (calories_needed / food_data["calories"]) * 100
                else:
                    # For other foods, use budget-based allocation
                    quantity_for_calories = (budget_per_food / food_data["price_per_100g"]) * 100

                # Cap quantities to reasonable amounts
                max_quantity = {
                    "cereals": 2000,  # 2kg max per cereal
                    "pulses": 1000,   # 1kg max per pulse
                    "proteins": 500,  # 500g max per protein
                    "dairy": 2000,    # 2L max per dairy
                    "vegetables": 1000, # 1kg max per vegetable
                    "fruits": 1000    # 1kg max per fruit
                }.get(category, 500)

                quantity = min(quantity_for_calories, max_quantity)

                # Only add if quantity is reasonable (>50g for most foods)
                min_quantity = 50 if category not in ["dairy"] else 200  # 200ml min for liquids
                if quantity >= min_quantity and plan["budget_remaining"] >= (quantity / 100) * food_data["price_per_100g"]:
                    cost = (quantity / 100) * food_data["price_per_100g"]

                    plan["groceries"][food] = plan["groceries"].get(food, 0) + quantity
                    plan["total_cost"] += cost
                    plan["total_calories"] += (quantity / 100) * food_data["calories"]
                    plan["total_protein"] += (quantity / 100) * food_data["protein"]
                    plan["total_iron"] += (quantity / 100) * food_data["iron"]
                    plan["total_vitamin_b12"] += (quantity / 100) * food_data["vitamin_b12"]
                    plan["budget_remaining"] -= cost

        # Check deficiency correction
        weekly_iron_target = self.nutrient_reqs["iron"] * 7 if "iron" in deficiencies else 0
        weekly_b12_target = self.nutrient_reqs["vitamin_b12"] * 7 if ("vitamin_b12" in deficiencies or "b12" in deficiencies) else 0

        plan["deficiencies_fixed"] = (
            plan["total_iron"] >= weekly_iron_target and
            plan["total_vitamin_b12"] >= weekly_b12_target
        )

        # Calculate nutrition efficiency score (0-100)
        calorie_score = min(plan["total_calories"] / targets["weekly_calories"], 1) * 25
        protein_score = min(plan["total_protein"] / targets["weekly_protein"], 1) * 25
        cost_score = (1 - plan["total_cost"] / weekly_budget) * 25
        deficiency_score = 25 if plan["deficiencies_fixed"] else 0

        plan["nutrition_efficiency_score"] = calorie_score + protein_score + cost_score + deficiency_score

        # Apply post-processing to round quantities and validate constraints
        final_plan = self.post_process_plan(plan)

        return final_plan

    def format_grocery_plan(self, plan: Dict) -> str:
        """Format the grocery plan for display"""
        output = []

        # Header
        output.append("🍎 **AI Nutrition Optimization Engine - Weekly Grocery Plan**")
        output.append("=" * 60)

        # Grocery List
        output.append("\n📋 **Weekly Grocery List:**")
        for food, quantity in plan["groceries"].items():
            food_data = self.food_db[food]
            cost = (quantity / 100) * food_data["price_per_100g"]
            output.append(f"• {food.replace('_', ' ').title()}: {quantity:.0f}g (₹{cost:.1f})")

        # Summary
        output.append(f"\n💰 **Total Cost:** ₹{plan['total_cost']:.1f}")
        output.append(f"💰 **Budget Remaining:** ₹{plan['budget_remaining']:.1f}")

        # Nutrition Summary
        output.append(f"\n🍎 **Total Weekly Calories:** {plan['total_calories']:.0f} / {plan['targets']['weekly_calories']:.0f}")
        output.append(f"💪 **Total Weekly Protein:** {plan['total_protein']:.1f}g / {plan['targets']['weekly_protein']:.1f}g")

        # Deficiency Status
        deficiency_status = "✅ Fixed" if plan["deficiencies_fixed"] else "❌ Not Fixed"
        output.append(f"🩺 **Deficiency Status:** {deficiency_status}")

        # Efficiency Score
        output.append(f"📊 **Nutrition Efficiency Score:** {plan['nutrition_efficiency_score']:.1f}/100")

        # Explanation
        output.append("\n📝 **Why these foods were selected:**")
        output.append("• **Rice/Wheat/Potatoes:** Cheap calorie sources for energy")
        output.append("• **Pulses (Dal/Chickpeas):** High protein, iron-rich, affordable")
        output.append("• **Vegetables:** Essential vitamins and fiber")
        output.append("• **Fruits:** Natural sweetness and micronutrients")
        if "eggs" in plan["groceries"] or "chicken" in plan["groceries"]:
            output.append("• **Eggs/Chicken:** Complete protein sources (if non-veg)")
        output.append("• **Milk/Curd:** Calcium and B12 sources")

        return final_plan

    def analyze_daily_intake(self, daily_data: Dict) -> List[str]:
        """
        Analyze daily food intake and generate personalized health insights.

        Args:
            daily_data: Dictionary containing daily intake information with keys:
                - calories: total calories consumed
                - protein: grams of protein
                - carbs: grams of carbohydrates
                - fats: grams of fats
                - sugar: grams of sugar
                - fiber: grams of fiber
                - sodium: milligrams of sodium
                - water: milliliters of water consumed
                - meals: list of meals consumed (optional)
                - weight: user's weight in kg
                - age: user's age
                - goal: fitness goal ('weight_loss', 'maintenance', 'muscle_gain')

        Returns:
            List of personalized health insights and recommendations
        """
        insights = []

        # Extract data with defaults
        calories = daily_data.get('calories', 0)
        protein = daily_data.get('protein', 0)
        carbs = daily_data.get('carbs', 0)
        fats = daily_data.get('fats', 0)
        sugar = daily_data.get('sugar', 0)
        fiber = daily_data.get('fiber', 0)
        sodium = daily_data.get('sodium', 0)
        water = daily_data.get('water', 0)
        weight = daily_data.get('weight', 70)
        age = daily_data.get('age', 30)
        goal = daily_data.get('goal', 'maintenance')
        meals = daily_data.get('meals', [])

        # Calculate recommended daily values based on user profile
        # Water: 30-35ml per kg body weight
        recommended_water = weight * 33

        # Protein: based on goal and weight
        if goal == 'muscle_gain':
            recommended_protein = weight * 1.6
        elif goal == 'weight_loss':
            recommended_protein = weight * 1.2
        else:  # maintenance
            recommended_protein = weight * 1.0

        # Age adjustment for protein (10% increase for 50+)
        if age > 50:
            recommended_protein *= 1.1

        # Fiber: 25-30g per day
        recommended_fiber = 25

        # Sugar: max 10% of calories from sugar (<50g for 2000 cal diet)
        max_sugar = calories * 0.1 / 4 if calories > 0 else 50

        # Sodium: <2300mg per day
        max_sodium = 2300

        # Carbohydrates: 45-65% of calories
        min_carbs = calories * 0.45 / 4 if calories > 0 else 225
        max_carbs = calories * 0.65 / 4 if calories > 0 else 325

        # Fats: 20-35% of calories
        min_fats = calories * 0.20 / 9 if calories > 0 else 44
        max_fats = calories * 0.35 / 9 if calories > 0 else 78

        # Calculate daily calorie needs (rough estimate)
        bmr = 10 * weight + 6.25 * (170) - 5 * age + 5  # Using average height
        activity_factor = 1.55  # moderately active
        daily_calorie_needs = bmr * activity_factor

        if goal == 'weight_loss':
            daily_calorie_needs -= 500
        elif goal == 'muscle_gain':
            daily_calorie_needs += 300

        # Generate insights based on analysis

        # 1. Water intake analysis
        if water < recommended_water * 0.7:
            insights.append("💧 Stay hydrated! You're drinking less than 70% of your recommended water intake. Aim for at least 8-10 glasses (2-2.5 liters) throughout the day.")
        elif water < recommended_water * 0.9:
            insights.append("💧 You're doing well with hydration, but could drink a bit more water. Try carrying a water bottle and setting reminders.")

        # 2. Fiber intake analysis
        if fiber < recommended_fiber * 0.6:
            insights.append("🥦 Your fiber intake is low. Include more fruits, vegetables, and whole grains in your meals. Try adding salads, whole grain roti, or fruits as snacks.")
        elif fiber < recommended_fiber * 0.8:
            insights.append("🥦 Good job on fiber! Add a bit more by including vegetables in every meal and choosing whole grain options.")

        # 3. Sugar intake analysis
        if sugar > max_sugar * 1.5:
            insights.append("🍬 Your sugar intake is quite high. Limit sugary drinks, desserts, and processed foods. Opt for fresh fruits instead of sugary snacks.")
        elif sugar > max_sugar:
            insights.append("🍬 Watch your sugar intake. Try reducing added sugars in tea/coffee and choosing unsweetened options.")

        # 4. Sodium intake analysis
        if sodium > max_sodium * 1.2:
            insights.append("🧂 Your sodium intake is high. Reduce salt in cooking, avoid processed foods, and limit packaged snacks. Use herbs and spices for flavor instead.")
        elif sodium > max_sodium:
            insights.append("🧂 Moderate your sodium intake by using less salt in cooking and choosing low-sodium options when available.")

        # 5. Protein intake analysis
        if protein < recommended_protein * 0.7:
            insights.append("💪 Your protein intake is low. Include more protein-rich foods like eggs, chicken, fish, paneer, or legumes in your meals.")
        elif protein < recommended_protein * 0.9:
            insights.append("💪 You're close to your protein goal! Add a bit more protein by including Greek yogurt, nuts, or lean meats.")

        # 6. Carbohydrate balance analysis
        if carbs < min_carbs:
            insights.append("🍚 Your carb intake is low. Include more whole grains, potatoes, and fruits to maintain energy levels throughout the day.")
        elif carbs > max_carbs:
            insights.append("🍚 Your carb intake is high. Balance it by including more vegetables and proteins, and choosing complex carbs over refined ones.")

        # 7. Fat quality analysis
        if fats < min_fats:
            insights.append("🥜 Your healthy fat intake could be higher. Include nuts, seeds, fish, or avocados for better nutrient absorption and heart health.")
        elif fats > max_fats:
            insights.append("🥜 Your fat intake is high. Focus on healthy fats from nuts, seeds, and olive oil, and reduce fried foods.")

        # 8. Calorie intake analysis (portion control)
        calorie_deviation = abs(calories - daily_calorie_needs) / daily_calorie_needs
        if calories > daily_calorie_needs * 1.2:
            insights.append("⚖️ Your calorie intake exceeds your daily needs. Consider portion control and include more vegetables to feel full with fewer calories.")
        elif calories < daily_calorie_needs * 0.8:
            insights.append("⚖️ Your calorie intake is low. Make sure you're eating enough to maintain energy levels and support your goals.")

        # 9. Meal timing analysis
        if len(meals) < 3:
            insights.append("🕐 Consider eating more regularly. Aim for 3 main meals and 1-2 snacks to maintain steady energy levels and prevent overeating.")
        elif len(meals) > 5:
            insights.append("🕐 You're eating frequently - that's great for metabolism! Just ensure portions are appropriate for your goals.")

        # 10. Processed foods analysis (based on available data)
        processed_food_indicators = []
        if sugar > max_sugar: processed_food_indicators.append("high sugar")
        if sodium > max_sodium: processed_food_indicators.append("high sodium")
        if fiber < recommended_fiber * 0.5: processed_food_indicators.append("low fiber")

        if len(processed_food_indicators) >= 2:
            insights.append("🍟 Limit processed and packaged foods. Focus on whole foods like fresh vegetables, fruits, whole grains, and lean proteins for better health.")

        # Add positive reinforcement if doing well
        good_indicators = []
        if water >= recommended_water * 0.9: good_indicators.append("hydration")
        if fiber >= recommended_fiber * 0.8: good_indicators.append("fiber")
        if protein >= recommended_protein * 0.9: good_indicators.append("protein")
        if min_carbs <= carbs <= max_carbs: good_indicators.append("carbs")
        if calorie_deviation < 0.1: good_indicators.append("calories")

        if len(good_indicators) >= 3:
            insights.append("🌟 Excellent job! You're doing great with your nutrition. Keep up the balanced approach!")

        # Return maximum 4 insights to avoid overwhelming the user
        return insights[:4]
        """
        Round grocery quantities to practical amounts based on food type
        """
        rounded_groceries = {}

        for food_name, quantity in groceries.items():
            if food_name not in self.food_db:
                # If food not in database, round to nearest 100g as fallback
                rounded_groceries[food_name] = round(quantity / 100) * 100
                continue

            food_data = self.food_db[food_name]
            category = food_data.get("category", "unknown")

            if category in ["cereal", "pulse", "vegetable", "fruit", "nut", "spice"]:
                # Grains & vegetables → nearest 100g
                rounded_groceries[food_name] = round(quantity / 100) * 100
            elif food_name == "eggs":
                # Eggs → whole numbers
                rounded_groceries[food_name] = round(quantity)
            elif food_name in ["chicken", "fish", "paneer"]:
                # Meat & paneer → nearest 50g
                rounded_groceries[food_name] = round(quantity / 50) * 50
            elif food_name == "milk":
                # Milk → nearest 500ml (assuming 1g = 1ml for milk)
                rounded_groceries[food_name] = round(quantity / 500) * 500
            else:
                # Other dairy (curd, etc.) → nearest 100g
                rounded_groceries[food_name] = round(quantity / 100) * 100

            # Ensure minimum quantity of 50g (except for eggs which can be 0)
            if food_name != "eggs" and rounded_groceries[food_name] < 50:
                rounded_groceries[food_name] = 50

        return rounded_groceries

    def recalculate_plan_totals(self, plan: Dict) -> Dict:
        """
        Recalculate total cost, calories, and protein after quantity changes
        """
        rounded_groceries = self.round_quantities(plan["groceries"])

        # Reset totals
        total_cost = 0
        total_calories = 0
        total_protein = 0
        total_iron = 0
        total_vitamin_b12 = 0

        # Recalculate based on rounded quantities
        for food_name, quantity in rounded_groceries.items():
            if food_name in self.food_db:
                food_data = self.food_db[food_name]
                cost = (quantity / 100) * food_data["price_per_100g"]
                calories = (quantity / 100) * food_data["calories"]
                protein = (quantity / 100) * food_data["protein"]
                iron = (quantity / 100) * food_data["iron"]
                vitamin_b12 = (quantity / 100) * food_data["vitamin_b12"]

                total_cost += cost
                total_calories += calories
                total_protein += protein
                total_iron += iron
                total_vitamin_b12 += vitamin_b12

        # Update plan with rounded quantities and recalculated totals
        updated_plan = plan.copy()
        updated_plan["groceries"] = rounded_groceries
        updated_plan["total_cost"] = total_cost
        updated_plan["total_calories"] = total_calories
        updated_plan["total_protein"] = total_protein
        updated_plan["total_iron"] = total_iron
        updated_plan["total_vitamin_b12"] = total_vitamin_b12
        updated_plan["budget_remaining"] = plan["weekly_budget"] - total_cost

        return updated_plan

    def validate_and_adjust_plan(self, plan: Dict) -> Dict:
        """
        Validate plan constraints and auto-adjust quantities if needed
        """
        targets = plan["targets"]
        weekly_budget = plan["weekly_budget"]
        target_calories = targets["weekly_calories"]
        target_protein = targets["weekly_protein"]

        # Check constraints
        calorie_deviation = abs(plan["total_calories"] - target_calories) / target_calories
        protein_ok = plan["total_protein"] >= target_protein
        budget_ok = plan["total_cost"] <= weekly_budget

        # If all constraints are met, return as-is
        if calorie_deviation <= 0.05 and protein_ok and budget_ok:
            return plan

        # Need adjustments - create adjustment plan
        adjusted_plan = plan.copy()
        adjusted_groceries = plan["groceries"].copy()

        # Strategy: Adjust calorie-dense foods to meet calorie target
        calorie_adjustment_needed = target_calories - plan["total_calories"]

        # Find foods that can be adjusted (prioritize cereals and proteins)
        adjustable_foods = []
        for food_name, quantity in adjusted_groceries.items():
            if food_name in self.food_db:
                food_data = self.food_db[food_name]
                category = food_data.get("category", "")
                if category in ["cereal", "pulse", "protein", "dairy"]:
                    adjustable_foods.append((food_name, quantity, food_data))

        # Sort by calorie density (calories per 100g)
        adjustable_foods.sort(key=lambda x: x[2]["calories"], reverse=True)

        # Distribute adjustment across top 2-3 foods
        num_foods_to_adjust = min(3, len(adjustable_foods))
        adjustment_per_food = calorie_adjustment_needed / num_foods_to_adjust

        for i in range(num_foods_to_adjust):
            food_name, current_quantity, food_data = adjustable_foods[i]
            calories_per_100g = food_data["calories"]

            # Calculate quantity adjustment needed
            quantity_adjustment = (adjustment_per_food / calories_per_100g) * 100

            # Apply adjustment with bounds
            new_quantity = current_quantity + quantity_adjustment

            # Apply category-specific rounding
            if food_data.get("category") in ["cereal", "pulse", "vegetable", "fruit"]:
                new_quantity = round(new_quantity / 100) * 100
            elif food_name in ["chicken", "fish", "paneer"]:
                new_quantity = round(new_quantity / 50) * 50
            elif food_name == "eggs":
                new_quantity = round(new_quantity)
            elif food_name == "milk":
                new_quantity = round(new_quantity / 500) * 500
            else:
                new_quantity = round(new_quantity / 100) * 100

            # Ensure reasonable bounds
            min_quantity = 50 if food_name != "eggs" else 0
            max_quantity = 3000  # 3kg max
            new_quantity = max(min_quantity, min(max_quantity, new_quantity))

            adjusted_groceries[food_name] = new_quantity

        # Recalculate totals with adjusted quantities
        return self.recalculate_plan_totals({
            **adjusted_plan,
            "groceries": adjusted_groceries
        })

    def post_process_plan(self, plan: Dict) -> Dict:
        """
        Apply post-processing: round quantities, recalculate totals, validate constraints
        """
        # Step 1: Round quantities to practical amounts
        rounded_plan = self.recalculate_plan_totals(plan)

        # Step 2: Validate constraints and auto-adjust if needed
        final_plan = self.validate_and_adjust_plan(rounded_plan)

        # Step 3: Calculate nutrition efficiency score
        targets = final_plan["targets"]
        calorie_score = min(100, 100 * (1 - abs(final_plan["total_calories"] - targets["weekly_calories"]) / targets["weekly_calories"]))
        protein_score = min(100, 100 * (final_plan["total_protein"] / targets["weekly_protein"]))
        budget_efficiency = min(100, 100 * (final_plan["total_cost"] / final_plan["weekly_budget"]))

        final_plan["nutrition_efficiency_score"] = (calorie_score * 0.4 + protein_score * 0.4 + budget_efficiency * 0.2)

        return final_plan

    def analyze_daily_intake(self, intake_data: Dict) -> List[str]:
        """
        Analyze daily nutrition intake and provide personalized health insights
        """
        insights = []

    def analyze_daily_intake(self, intake_data: Dict) -> List[str]:
        """
        Analyze daily nutrition intake and provide personalized health insights
        """
        insights = []

        # Extract data with validation
        calories = intake_data.get('calories', 0) or 0
        protein = intake_data.get('protein', 0) or 0
        carbs = intake_data.get('carbs', 0) or 0
        fats = intake_data.get('fats', 0) or 0
        sugar = intake_data.get('sugar', 0) or 0
        fiber = intake_data.get('fiber', 0) or 0
        sodium = intake_data.get('sodium', 0) or 0
        water = intake_data.get('water', 0) or 0
        weight = intake_data.get('weight', 70) or 70
        age = intake_data.get('age', 30) or 30
        goal = intake_data.get('goal', 'maintenance') or 'maintenance'
        meals = intake_data.get('meals', [])

        # Calculate recommended values based on weight and goal
        if goal == 'weight_loss':
            recommended_calories = weight * 25  # 25 kcal/kg for weight loss
            recommended_protein = weight * 1.2  # 1.2g/kg for weight loss
        elif goal == 'muscle_gain':
            recommended_calories = weight * 35  # 35 kcal/kg for muscle gain
            recommended_protein = weight * 1.6  # 1.6g/kg for muscle gain
        else:  # maintenance
            recommended_calories = weight * 30  # 30 kcal/kg for maintenance
            recommended_protein = weight * 1.0  # 1.0g/kg for maintenance

        print(f"DEBUG: recommended_calories={recommended_calories}, recommended_protein={recommended_protein}")

        # Generate insights

        # 1. Hydration analysis
        if water < 2000:
            deficit = 2000 - water
            insights.append(f"💧 Increase water intake by {deficit}ml. Aim for at least 2-3 liters daily for optimal hydration and metabolism.")
        elif water >= 2500:
            insights.append("💧 Excellent hydration! You're drinking enough water to support digestion and nutrient absorption.")

        # 2. Fiber analysis
        recommended_fiber = 25  # g per day
        if fiber < 15:
            deficit = 15 - fiber
            insights.append(f"🌾 Fiber intake is low. Add {deficit}g more fiber through vegetables, fruits, and whole grains to improve digestion and heart health.")
        elif fiber >= 25:
            insights.append("🌾 Great fiber intake! This supports healthy digestion and helps maintain stable blood sugar levels.")

        # 3. Sugar analysis
        max_sugar = calories * 0.1 / 4  # Max 10% of calories from sugar
        if sugar > max_sugar:
            excess = sugar - max_sugar
            insights.append(f"🍬 Sugar intake is high ({sugar:.1f}g). Reduce by {excess:.1f}g by limiting sweets and sugary drinks to prevent energy crashes and support weight goals.")
        elif sugar <= max_sugar * 0.5:
            insights.append("🍬 Good sugar control! Your intake supports stable energy levels and metabolic health.")

        # 4. Sodium analysis
        max_sodium = 2300  # mg per day (WHO recommendation)
        if sodium > max_sodium:
            excess = sodium - max_sodium
            insights.append(f"🧂 Sodium intake is high ({sodium}mg). Reduce by {excess}mg by using less salt and processed foods to support heart health and blood pressure.")
        elif sodium <= 1500:
            insights.append("🧂 Excellent sodium control! This supports healthy blood pressure and cardiovascular wellness.")

        # 5. Protein analysis
        protein_ratio = (protein * 4) / calories  # Protein calories as % of total
        if protein < recommended_protein * 0.8:
            deficit = recommended_protein - protein
            insights.append(f"🥩 Protein intake needs improvement. Add {deficit:.1f}g more protein through lean meats, dairy, or legumes to support muscle maintenance and satiety.")
        elif protein >= recommended_protein:
            insights.append("🥩 Strong protein intake! This supports muscle health, metabolism, and helps you feel full longer.")

        # 6. Carbohydrate analysis
        carb_calories = carbs * 4
        carb_ratio = carb_calories / calories
        if carb_ratio < 0.45:
            min_carbs = (recommended_calories * 0.45) / 4
            deficit = min_carbs - carbs
            insights.append(f"🍞 Carbohydrate intake is low. Consider adding {deficit:.1f}g more complex carbs from whole grains and vegetables for sustained energy.")
        elif carb_ratio > 0.65:
            max_carbs = (recommended_calories * 0.65) / 4
            excess = carbs - max_carbs
            insights.append(f"🍞 Carbohydrate intake is high. Reduce by {excess:.1f}g if focusing on weight loss, or ensure they're from whole food sources.")

        # 7. Fat analysis
        fat_calories = fats * 9
        fat_ratio = fat_calories / calories
        if fat_ratio < 0.2:
            min_fats = (recommended_calories * 0.2) / 9
            deficit = min_fats - fats
            insights.append(f"🥑 Healthy fat intake is low. Add {deficit:.1f}g more healthy fats from avocados, nuts, and olive oil for hormone health and nutrient absorption.")
        elif fat_ratio > 0.35:
            max_fats = (recommended_calories * 0.35) / 9
            excess = fats - max_fats
            insights.append(f"🥑 Fat intake is high ({fat_ratio:.1%} of calories). Consider reducing by {excess:.1f}g while ensuring adequate healthy fat sources.")

        # 8. Calorie analysis
        calorie_deviation = abs(calories - recommended_calories) / recommended_calories
        if calorie_deviation > 0.2:
            if calories > recommended_calories:
                excess = calories - recommended_calories
                insights.append(f"🔥 Calorie intake is {excess:.0f} above your target. Consider portion control or increased activity to align with your {goal.replace('_', ' ')} goals.")
            else:
                deficit = recommended_calories - calories
                insights.append(f"⚡ Calorie intake is {deficit:.0f} below your target. You may need more food volume to meet energy needs and support your {goal.replace('_', ' ')} goals.")
        else:
            insights.append(f"🎯 Calorie intake is well-aligned with your {goal.replace('_', ' ')} goals. Great job maintaining consistency!")

        # 9. Meal timing analysis
        if len(meals) < 3:
            insights.append("🕐 Consider eating more regularly. Aim for 3 main meals and 1-2 snacks to maintain steady energy and metabolism.")
        elif len(meals) >= 4:
            insights.append("🕐 Good meal frequency! Regular eating supports stable blood sugar and sustained energy throughout the day.")

        # 10. Overall assessment
        positive_count = sum(1 for insight in insights if any(emoji in insight for emoji in ['💧', '🌾', '🍬', '🧂', '🥩', '🍞', '🥑', '🎯', '🕐']))
        if positive_count >= 7:
            insights.append("🏆 Excellent nutrition profile! You're making great choices across all major nutrient categories. Keep up the outstanding work!")
        elif positive_count >= 5:
            insights.append("👍 Good overall nutrition! You're doing well in most areas. Focus on the highlighted improvement opportunities for even better results.")
        else:
            insights.append("💪 Room for improvement in several areas. Start with 2-3 key changes from the insights above to make meaningful progress toward better health.")

        return insights