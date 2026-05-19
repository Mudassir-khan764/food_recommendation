# 🚀 Modern UI Quick Reference Guide

## Get Started in 60 Seconds

### Step 1: Link Resources
```html
<!-- In your HTML <head> -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="{{ url_for('static', filename='css/modern.css') }}" rel="stylesheet">
<script src="{{ url_for('static', filename='js/modern-utils.js') }}"></script>
```

### Step 2: Use Components

**Button Examples:**
```html
<!-- Primary (Main action) -->
<button class="btn btn-primary">Save Changes</button>

<!-- Secondary (Alternative) -->
<button class="btn btn-secondary">Cancel</button>

<!-- Success -->
<button class="btn btn-success">Confirm</button>

<!-- Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-lg">Large</button>
```

**Card Examples:**
```html
<!-- Basic Card -->
<div class="card">
    <div class="card-header">
        <h3>Title</h3>
    </div>
    <div class="card-body">Content</div>
</div>

<!-- Gradient Card -->
<div class="card card-gradient">
    <h3>Premium Card</h3>
</div>
```

**Form Examples:**
```html
<!-- Text Input -->
<div class="form-group">
    <label class="form-label">Email</label>
    <input type="email" class="form-input" placeholder="your@email.com">
</div>

<!-- Select -->
<div class="form-group">
    <label class="form-label">Category</label>
    <select class="form-select">
        <option>Choose...</option>
        <option>Option 1</option>
    </select>
</div>

<!-- Checkbox -->
<div class="form-check">
    <input type="checkbox" id="agree">
    <label for="agree">I agree</label>
</div>
```

**Grid Examples:**
```html
<!-- 2-column responsive grid -->
<div class="grid grid-2">
    <div class="card">Item 1</div>
    <div class="card">Item 2</div>
    <div class="card">Item 3</div>
</div>

<!-- 3-column responsive grid -->
<div class="grid grid-3">
    <div class="card">Item 1</div>
    <div class="card">Item 2</div>
    <div class="card">Item 3</div>
</div>
```

### Step 3: Use JavaScript Utils

**Show Notifications:**
```javascript
Toast.success('Saved successfully!');
Toast.error('An error occurred!');
Toast.info('Here\'s some info');
Toast.warning('Be careful!');
```

**Loading States:**
```javascript
Loader.show();  // Show loading
// ... do something ...
Loader.hide();  // Hide loading
```

**API Requests:**
```javascript
// GET
const { success, data } = await API.get('/api/meals');

// POST
const { success, data } = await API.post('/api/meals', {
    name: 'Grilled Chicken',
    calories: 280
});

// Check result
if (success) {
    Toast.success('Meal added!');
} else {
    Toast.error('Failed to add meal');
}
```

**DOM Manipulation:**
```javascript
// Find elements
const element = DOM.query('.my-element');
const elements = DOM.queryAll('.my-elements');

// Create element
const newCard = DOM.create('div', 'card', '<p>New Card</p>');

// Show/Hide
DOM.hide(element);
DOM.show(element);

// Add/Remove classes
DOM.addClass(element, 'active');
DOM.removeClass(element, 'active');
DOM.toggleClass(element, 'active');
```

**Animations:**
```javascript
// Fade in
Animations.fadeIn(element);

// Slide up
Animations.slideUp(element);

// Scale in
Animations.scale(element);
```

---

## Common Patterns

### Login Form
```html
<div class="login-form-wrapper">
    <div class="login-form-header">
        <h2>Welcome Back</h2>
        <p>Sign in to continue</p>
    </div>
    
    <form class="login-form">
        <div class="form-group">
            <input type="email" class="form-input" placeholder="Email">
        </div>
        
        <div class="form-group">
            <input type="password" class="form-input" placeholder="Password">
        </div>
        
        <button type="submit" class="btn btn-primary btn-block">
            Sign In
        </button>
    </form>
</div>
```

### Dashboard Stats
```html
<div class="grid grid-4">
    <div class="stat-card">
        <div class="stat-icon">🔥</div>
        <div class="stat-value">1,280</div>
        <div class="stat-label">Calories</div>
    </div>
    
    <div class="stat-card">
        <div class="stat-icon">💪</div>
        <div class="stat-value">85g</div>
        <div class="stat-label">Protein</div>
    </div>
</div>
```

### Meal Card
```html
<div class="meal-card">
    <div class="meal-image">
        🍗
        <div class="meal-badge">Recommended</div>
    </div>
    
    <div class="meal-content">
        <div class="meal-name">Grilled Chicken</div>
        <div class="meal-description">with vegetables</div>
        
        <div class="meal-nutrition">
            <div class="nutrition-item">
                <div class="nutrition-value">280</div>
                <div class="nutrition-label">Cal</div>
            </div>
            <div class="nutrition-item">
                <div class="nutrition-value">35g</div>
                <div class="nutrition-label">Protein</div>
            </div>
        </div>
        
        <div class="meal-footer">
            <button class="btn-meal">View</button>
            <button class="btn-meal btn-meal-primary">Add</button>
        </div>
    </div>
</div>
```

### Modal/Overlay
```html
<div class="modal" style="
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050;
">
    <div class="card" style="max-width: 500px;">
        <div class="card-header">
            <h3>Confirm Action</h3>
        </div>
        <div class="card-body">
            <p>Are you sure?</p>
        </div>
        <div class="card-footer">
            <button class="btn btn-primary">Confirm</button>
            <button class="btn btn-secondary">Cancel</button>
        </div>
    </div>
</div>
```

---

## Color Usage

### When to Use Each Color

**Primary (Purple/Blue)** - Main brand, primary actions
```html
<button class="btn btn-primary">Use me for main CTAs</button>
<div class="btn btn-primary">Primary navigation items</div>
```

**Accent (Cyan)** - Featured, eye-catching
```html
<button class="btn btn-accent">Use me for featured actions</button>
<div class="meal-badge">Featured tag</div>
```

**Success (Green)** - Confirmations, positive actions
```html
<button class="btn btn-success">Save</button>
<div class="stat-change">↑ 15% improvement</div>
```

**Danger (Red)** - Destructive, delete actions
```html
<button class="btn btn-danger">Delete</button>
```

**Warning (Orange)** - Warnings, caution
```html
<div class="alert alert-warning">Be careful!</div>
```

---

## Responsive Design Tips

### Mobile-First Approach
```css
/* Base styles (mobile) */
.card { grid-template-columns: 1fr; }

/* Tablet and up */
@media (min-width: 768px) {
    .card { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop and up */
@media (min-width: 1024px) {
    .card { grid-template-columns: repeat(4, 1fr); }
}
```

### Sidebar Behavior
```css
/* Desktop: Sidebar visible */
.sidebar { transform: translateX(0); }
.main-content { margin-left: 280px; }

/* Mobile: Sidebar hidden */
@media (max-width: 768px) {
    .sidebar { transform: translateX(-100%); }
    .main-content { margin-left: 0; }
}
```

---

## Performance Tips

### 1. Lazy Load Images
```html
<img src="food.jpg" loading="lazy" alt="Food">
```

### 2. Use CSS Variables
```css
/* Good - CSS variable (can be changed at runtime) */
color: var(--color-primary);

/* Bad - Hard-coded value */
color: #667eea;
```

### 3. Debounce Search
```javascript
const searchInput = document.querySelector('#search');
const handleSearch = debounce((e) => {
    // Search logic
}, 300);
searchInput.addEventListener('input', handleSearch);
```

### 4. Use Transitions Instead of Animations for Simple Effects
```css
/* Good - For simple hover effects */
transition: all 0.3s ease;

/* Avoid - Unnecessary animations */
animation: complex-animation 10s infinite;
```

---

## Accessibility Checklist

- [ ] All buttons have descriptive text
- [ ] Form labels are associated with inputs
- [ ] Color is not the only indicator (use icons too)
- [ ] Sufficient color contrast (WCAG AA)
- [ ] Keyboard navigation works
- [ ] Images have alt text
- [ ] Focus states are visible
- [ ] Screen reader friendly

---

## Browser Compatibility

### Supported Features by Browser

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS Grid | ✅ | ✅ | ✅ | ✅ |
| Flexbox | ✅ | ✅ | ✅ | ✅ |
| CSS Variables | ✅ | ✅ | ✅ | ✅ |
| Backdrop Filter | ✅ | ✅ | ✅ (iOS 14+) | ✅ |
| Gradients | ✅ | ✅ | ✅ | ✅ |
| Transitions | ✅ | ✅ | ✅ | ✅ |
| Animations | ✅ | ✅ | ✅ | ✅ |

---

## Debugging

### Check CSS Loading
```javascript
// In console
getComputedStyle(document.body).getPropertyValue('--color-primary')
// Should output: #667eea
```

### Check JavaScript Loaded
```javascript
console.log(typeof Toast); // Should be 'object'
console.log(typeof API);   // Should be 'object'
```

### Common Issues

**Issue: Buttons not styled**
- Check `modern.css` is linked
- Verify class names are correct
- Check for CSS conflicts

**Issue: Sidebar not showing**
- Check `modern.css` is linked
- Verify sidebar HTML structure
- Check z-index conflicts

**Issue: Animations stuttering**
- Close other tabs/apps
- Check browser performance
- Reduce animation duration

---

## Integration with Flask

### Rendering Templates
```python
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard-modern.html')
```

### Passing Data to Template
```python
@app.route('/dashboard')
def dashboard():
    user_data = {
        'name': 'John Doe',
        'calories': 1280,
        'protein': 85
    }
    return render_template('dashboard-modern.html', user=user_data)
```

### Using Data in HTML
```html
<h1>Welcome {{ user.name }}</h1>
<div class="stat-value">{{ user.calories }}</div>
```

---

## Next Steps

1. **Customize colors** for your brand
2. **Add your logo** to navbar
3. **Connect API endpoints** to buttons
4. **Add form validation** with JavaScript
5. **Optimize images** for performance
6. **Test on mobile devices**
7. **Get feedback** from users
8. **Deploy to production**

---

## Need Help?

- Check `MODERN_UI_DOCUMENTATION.md` for detailed docs
- Review component examples in templates
- Test in browser DevTools
- Check browser console for errors

**Good Luck! 🚀**
