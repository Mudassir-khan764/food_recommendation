// Enhanced Dashboard JavaScript with advanced validation and meal planning
class AdvancedMealPlannerApp {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.formData = {};
        this.isLoading = false;
        this.validationRules = this.initValidationRules();
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initAnimations();
        this.initFormValidation();
        this.setupRealTimeValidation();
    }
    
    initValidationRules() {
        return {
            age: { required: true, min: 1, max: 120, message: 'Age must be between 1 and 120' },
            gender: { required: true, message: 'Please select your gender' },
            height: { required: true, min: 100, max: 250, message: 'Height must be between 100-250 cm' },
            weight: { required: true, min: 30, max: 300, message: 'Weight must be between 30-300 kg' },
            activity_level: { required: true, message: 'Please select your activity level' },
            primary_goal: { required: true, message: 'Please select your primary goal' },
            diet_type: { required: true, message: 'Please select your diet type' }
        };
    }
    
    bindEvents() {
        const form = document.getElementById('mealPlanForm');
        if (form) {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        }
        
        // Add input event listeners for real-time validation
        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', this.handleInputChange.bind(this));
            input.addEventListener('blur', this.validateField.bind(this));
        });
        
        // Action button events
        document.addEventListener('click', (e) => {
            if (e.target.id === 'downloadPDF' || e.target.closest('#downloadPDF')) {
                this.downloadPDF();
            }
            if (e.target.id === 'regeneratePlan' || e.target.closest('#regeneratePlan')) {
                this.regeneratePlan();
            }
        });
    }
    
    setupRealTimeValidation() {
        // Target weight validation based on current weight
        const weightInput = document.getElementById('weight');
        const targetWeightInput = document.getElementById('target_weight');
        
        if (weightInput && targetWeightInput) {
            weightInput.addEventListener('input', () => {
                const currentWeight = parseFloat(weightInput.value);
                if (currentWeight && !targetWeightInput.value) {
                    targetWeightInput.placeholder = `Current: ${currentWeight} kg`;
                }
            });
        }
    }
    
    initAnimations() {
        // Animate elements on page load
        this.animateOnLoad();
    }
    
    animateOnLoad() {
        // Animate form sections with staggered delay
        const formSections = document.querySelectorAll('.form-section');
        formSections.forEach((section, index) => {
            setTimeout(() => {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }
    
    initFormValidation() {
        // Add custom validation styles
        const style = document.createElement('style');
        style.textContent = `
            .modern-input.is-invalid, .modern-select.is-invalid {
                border-color: #ef4444;
                box-shadow: 0 0 0 0.2rem rgba(239, 68, 68, 0.1);
            }
            .modern-input.is-valid, .modern-select.is-valid {
                border-color: #10b981;
                box-shadow: 0 0 0 0.2rem rgba(16, 185, 129, 0.1);
            }
            .form-section {
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.5s ease;
            }
        `;
        document.head.appendChild(style);
    }
    
    validateField(event) {
        const field = event.target;
        const fieldId = field.id;
        const value = field.value.trim();
        
        // Clear previous validation
        this.clearFieldValidation(field);
        
        // Check validation rules
        const rule = this.validationRules[fieldId];
        if (!rule) return true;
        
        let isValid = true;
        let message = '';
        
        // Required field check
        if (rule.required && !value) {
            isValid = false;
            message = rule.message || 'This field is required';
        }
        
        // Numeric range validation
        if (value && rule.min !== undefined && parseFloat(value) < rule.min) {
            isValid = false;
            message = rule.message;
        }
        
        if (value && rule.max !== undefined && parseFloat(value) > rule.max) {
            isValid = false;
            message = rule.message;
        }
        
        // Apply validation styles
        if (value) {
            if (isValid) {
                field.classList.remove('is-invalid');
                field.classList.add('is-valid');
            } else {
                field.classList.remove('is-valid');
                field.classList.add('is-invalid');
                this.showFieldError(field, message);
            }
        } else {
            field.classList.remove('is-valid', 'is-invalid');
        }
        
        return isValid;
    }
    
    clearFieldValidation(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        field.classList.remove('is-valid', 'is-invalid');
    }
    
    showFieldError(field, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            color: #ef4444;
            font-size: 0.875rem;
            margin-top: 0.25rem;
            display: block;
        `;
        field.parentNode.appendChild(errorDiv);
    }
    
    validateForm() {
        let isFormValid = true;
        const requiredFields = ['age', 'gender', 'height', 'weight', 'activity_level', 'primary_goal', 'diet_type'];
        
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field && !this.validateField({ target: field })) {
                isFormValid = false;
            }
        });
        
        return isFormValid;
    }
    
    handleInputChange(event) {
        const field = event.target;
        
        // Add subtle animation to the field
        field.style.transform = 'scale(1.02)';
        setTimeout(() => {
            field.style.transform = 'scale(1)';
        }, 150);
    }
    
    collectFormData() {
        const allergies = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.value);
            
        return {
            // Personal Details
            age: parseInt(document.getElementById('age').value),
            gender: document.getElementById('gender').value,
            height: parseFloat(document.getElementById('height').value),
            weight: parseFloat(document.getElementById('weight').value),
            body_fat: parseFloat(document.getElementById('body_fat').value) || null,
            
            // Health & Lifestyle
            activity_level: document.getElementById('activity_level').value,
            medical_conditions: document.getElementById('medical_conditions').value,
            water_intake: parseFloat(document.getElementById('water_intake').value) || 2.5,
            sleep_duration: parseFloat(document.getElementById('sleep_duration').value) || 8,
            digestive_issues: document.getElementById('digestive_issues').value === 'Yes',
            
            // Diet Preferences
            diet_type: document.getElementById('diet_type').value,
            cuisine_preference: document.getElementById('cuisine_preference').value,
            budget_level: document.getElementById('budget_level').value,
            cooking_time: document.getElementById('cooking_time').value,
            meals_per_day: parseInt(document.getElementById('meals_per_day').value),
            allergies: allergies,
            
            // Fitness Goals
            primary_goal: document.getElementById('primary_goal').value,
            target_weight: parseFloat(document.getElementById('target_weight').value) || null,
            workout_days: parseInt(document.getElementById('workout_days').value),
            protein_preference: document.getElementById('protein_preference').value
        };
    }
    
    async handleFormSubmit(event) {
        event.preventDefault();
        
        if (this.isLoading) return;
        
        // Validate form
        if (!this.validateForm()) {
            this.showNotification('Please fill in all required fields correctly', 'error');
            return;
        }
        
        this.isLoading = true;
        
        // Show loading state
        this.showLoading();
        
        // Collect form data
        const formData = this.collectFormData();
        
        try {
            const response = await fetch('/generate-meal-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            // Simulate minimum loading time for better UX
            await this.delay(2000);
            
            if (data.success) {
                this.displayMealPlan(data);
                this.showNotification('Advanced meal plan generated successfully!', 'success');
            } else {
                this.showError(data.error);
                this.showNotification(data.error, 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('An error occurred while generating your meal plan. Please try again.');
            this.showNotification('Something went wrong. Please try again.', 'error');
        } finally {
            this.hideLoading();
            this.isLoading = false;
        }
    }
    
    showLoading() {
        const loadingSpinner = document.getElementById('loadingSpinner');
        const resultsDiv = document.getElementById('mealPlanResults');
        const errorDiv = document.getElementById('errorMessage');
        
        if (loadingSpinner) {
            loadingSpinner.style.display = 'block';
        }
        
        if (resultsDiv) resultsDiv.style.display = 'none';
        if (errorDiv) errorDiv.style.display = 'none';
        
        // Update submit button
        const submitBtn = document.querySelector('#mealPlanForm button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Generating Advanced Plan...</span>';
        }
    }
    
    hideLoading() {
        const loadingSpinner = document.getElementById('loadingSpinner');
        const submitBtn = document.querySelector('#mealPlanForm button[type="submit"]');
        
        if (loadingSpinner) {
            setTimeout(() => {
                loadingSpinner.style.display = 'none';
            }, 300);
        }
        
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span class="btn-icon">🤖</span><span class="btn-text">Generate My Advanced Meal Plan</span><span class="btn-arrow">→</span>';
        }
    }
    
    displayMealPlan(data) {
        const resultsDiv = document.getElementById('mealPlanResults');
        if (!resultsDiv) return;
        
        // Update user summary
        this.updateUserSummary(data.user_summary);
        
        // Update macro breakdown
        this.updateMacroBreakdown(data.macros);
        
        // Update meal cards
        this.updateMealCard('breakfast', data.meal_plan.breakfast);
        this.updateMealCard('lunch', data.meal_plan.lunch);
        this.updateMealCard('snack', data.meal_plan.snack);
        this.updateMealCard('dinner', data.meal_plan.dinner);
        
        // Update tips
        this.updateTips(data.health_tips, data.hydration_tips);
        
        // Show results with animation
        resultsDiv.style.display = 'block';
        resultsDiv.classList.add('fade-in');
        
        // Scroll to results
        setTimeout(() => {
            resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 600);
    }
    
    updateUserSummary(summary) {
        document.getElementById('bmiValue').textContent = summary.bmi;
        document.getElementById('bmrValue').textContent = `${summary.bmr} cal`;
        document.getElementById('dailyCalories').textContent = `${summary.daily_calories} cal`;
    }
    
    updateMacroBreakdown(macros) {
        document.getElementById('proteinTarget').textContent = `${macros.protein}g`;
        document.getElementById('carbsTarget').textContent = `${macros.carbs}g`;
        document.getElementById('fatsTarget').textContent = `${macros.fats}g`;
    }
    
    updateMealCard(mealType, mealData) {
        const caloriesEl = document.getElementById(`${mealType}Calories`);
        const itemsEl = document.getElementById(`${mealType}Items`);
        const macrosEl = document.getElementById(`${mealType}Macros`);
        
        if (caloriesEl) {
            caloriesEl.textContent = `${mealData.calories} cal`;
        }
        
        if (itemsEl) {
            itemsEl.innerHTML = '';
            mealData.items.forEach((item, index) => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'meal-item';
                itemDiv.innerHTML = `
                    <div class="item-name">${item.name}</div>
                    <div class="item-calories">${item.calories} cal</div>
                `;
                itemDiv.style.opacity = '0';
                itemDiv.style.transform = 'translateX(-20px)';
                itemsEl.appendChild(itemDiv);
                
                // Stagger item animations
                setTimeout(() => {
                    itemDiv.style.transition = 'all 0.3s ease';
                    itemDiv.style.opacity = '1';
                    itemDiv.style.transform = 'translateX(0)';
                }, index * 100);
            });
        }
        
        if (macrosEl && mealData.macros) {
            macrosEl.innerHTML = `
                <div class="meal-macro">
                    <div class="meal-macro-label">Protein</div>
                    <div class="meal-macro-value">${mealData.macros.protein}g</div>
                </div>
                <div class="meal-macro">
                    <div class="meal-macro-label">Carbs</div>
                    <div class="meal-macro-value">${mealData.macros.carbs}g</div>
                </div>
                <div class="meal-macro">
                    <div class="meal-macro-label">Fats</div>
                    <div class="meal-macro-value">${mealData.macros.fats}g</div>
                </div>
            `;
        }
    }
    
    updateTips(healthTips, hydrationTips) {
        const healthTipsEl = document.getElementById('healthTips');
        const hydrationTipsEl = document.getElementById('hydrationTips');
        
        if (healthTipsEl && healthTips) {
            healthTipsEl.innerHTML = `<ul>${healthTips.map(tip => `<li>${tip}</li>`).join('')}</ul>`;
        }
        
        if (hydrationTipsEl && hydrationTips) {
            hydrationTipsEl.innerHTML = `<ul>${hydrationTips.map(tip => `<li>${tip}</li>`).join('')}</ul>`;
        }
    }
    
    downloadPDF() {
        // Create a simple PDF download functionality
        const mealPlanData = this.getMealPlanData();
        if (!mealPlanData) {
            this.showNotification('No meal plan to download', 'error');
            return;
        }
        
        // For now, create a text file with meal plan data
        const content = this.formatMealPlanForDownload(mealPlanData);
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = 'meal-plan.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('Meal plan downloaded successfully!', 'success');
    }
    
    regeneratePlan() {
        const form = document.getElementById('mealPlanForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
    
    getMealPlanData() {
        const resultsDiv = document.getElementById('mealPlanResults');
        return resultsDiv && resultsDiv.style.display !== 'none' ? true : false;
    }
    
    formatMealPlanForDownload(data) {
        return `
NutriAI - Personalized Meal Plan
================================

Generated on: ${new Date().toLocaleDateString()}

BREAKFAST:
${this.getMealItems('breakfast')}

LUNCH:
${this.getMealItems('lunch')}

SNACK:
${this.getMealItems('snack')}

DINNER:
${this.getMealItems('dinner')}

HEALTH TIPS:
${this.getTipsText('healthTips')}

HYDRATION TIPS:
${this.getTipsText('hydrationTips')}
        `;
    }
    
    getMealItems(mealType) {
        const itemsEl = document.getElementById(`${mealType}Items`);
        if (!itemsEl) return 'No items found';
        
        const items = Array.from(itemsEl.querySelectorAll('.meal-item'));
        return items.map(item => {
            const name = item.querySelector('.item-name')?.textContent || '';
            const calories = item.querySelector('.item-calories')?.textContent || '';
            return `- ${name} (${calories})`;
        }).join('\n');
    }
    
    getTipsText(elementId) {
        const tipsEl = document.getElementById(elementId);
        if (!tipsEl) return 'No tips available';
        
        const items = Array.from(tipsEl.querySelectorAll('li'));
        return items.map(item => `- ${item.textContent}`).join('\n');
    }
    
    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.querySelector('.error-text').textContent = message;
            errorDiv.style.display = 'block';
            errorDiv.classList.add('fade-in');
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} notification-toast`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle';
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${icon} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AdvancedMealPlannerApp();
});