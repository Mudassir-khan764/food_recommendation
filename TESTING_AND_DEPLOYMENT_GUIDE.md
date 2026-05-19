# Testing & Deployment Guide

## 🎯 Quick Start: Verify the Fixes

### Step 1: Start MongoDB
```bash
# Windows
mongod

# Or if using MongoDB Atlas, ensure connection string in database.py has:
# serverSelectionTimeoutMS=5000
# connectTimeoutMS=5000
```

### Step 2: Start Flask Server
```bash
cd AI-Meal-Planner
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 WARNING: This is a development server. Do not use it in production.
```

### Step 3: Open Browser
```
http://localhost:5000
```

You should see the login page (no "Loading..." hang).

---

## ✅ Test Cases - Complete Flow

### Test 1: Login Flow
**Goal:** Verify login works and session persists

1. Navigate to `http://localhost:5000/login`
2. Expected: Login form loads instantly (no hang)
3. Enter valid email and password
4. Click login
5. Expected: ✅ Redirect to `/dashboard`
6. Refresh page
7. Expected: ✅ Dashboard still loads (session persisted)

**If fails:**
- Check MongoDB is running
- Check user exists in database
- Check Flask logs for error messages

---

### Test 2: Signup Flow
**Goal:** Verify signup with validation works

1. Navigate to `http://localhost:5000/signup`
2. Try entering duplicate email (if exists)
3. Expected: ❌ "Email already registered" error (409 Conflict)
4. Try submitting empty form
5. Expected: ❌ Validation error
6. Enter valid data
7. Click signup
8. Expected: ✅ Redirect to dashboard with new account

**Expected Status Codes:**
- Duplicate email: `409 Conflict`
- Missing fields: `400 Bad Request`
- Success: `200 OK`

---

### Test 3: Track Page Loading
**Goal:** Verify no "Loading..." hang on /track

1. Login to account
2. Navigate to `http://localhost:5000/track`
3. Expected: ✅ Page loads within 2 seconds
4. Food search dropdown should populate
5. Add a food item
6. Expected: ✅ Food appears in today's meals instantly

**If hangs ("Loading..."):**
- MongoDB connection timeout (5 seconds wait)
- Check MongoDB is running: `ping localhost:27017`
- Restart Flask server

---

### Test 4: Search Foods AJAX
**Goal:** Verify search returns proper HTTP status codes

1. On `/track` page, type in food search box
2. Type "pi" (for pizza)
3. Expected: ✅ Results dropdown shows matching foods
4. Expected response code: `200 OK`

**Test with curl:**
```bash
curl "http://localhost:5000/api/search_foods?q=pi" -w "\n%{http_code}\n"
```

Expected output:
```json
[
  {
    "id": "...",
    "name": "Pizza",
    "calories": 250,
    ...
  }
]
200
```

---

### Test 5: Add Food to Meal
**Goal:** Verify AJAX POST returns proper status codes

1. On `/track` page, select a food from search
2. Enter quantity
3. Click "Add Food"
4. Expected: ✅ Food appears in "Today's Meals" section
5. Check Network tab for response code
6. Expected: `200 OK` with success message

**Test with curl:**
```bash
# First, get a session cookie
curl -c cookies.txt -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"pass"}'

# Then add food with same cookie
curl -b cookies.txt -X POST http://localhost:5000/api/add_food \
  -H "Content-Type: application/json" \
  -d '{"food_id":"<food_id>","quantity":100}' \
  -w "\n%{http_code}\n"
```

Expected: `200 OK` response

---

### Test 6: Remove Food from Meal
**Goal:** Verify DELETE returns proper status codes

1. On `/track` page, hover over a food item in today's meals
2. Click delete button
3. Expected: ✅ Food disappears from list
4. Expected status code: `200 OK`

**Test with curl:**
```bash
curl -b cookies.txt -X DELETE \
  http://localhost:5000/api/remove_food/<food_log_id> \
  -w "\n%{http_code}\n"
```

Expected: `200 OK` response

---

### Test 7: Profile Page Update Goals
**Goal:** Verify goal updates work with validation

1. Navigate to `/profile`
2. Expected: ✅ Page loads instantly with no hang
3. Modify calorie goal to negative number (e.g., -100)
4. Click save
5. Expected: ❌ Error message "Goals must be non-negative"
6. Expected status code: `400 Bad Request`

7. Enter valid goals (e.g., 2000 calories)
8. Click save
9. Expected: ✅ Success message, page updates
10. Expected status code: `200 OK`

**Test with curl:**
```bash
# Valid update
curl -b cookies.txt -X POST http://localhost:5000/api/update_goals \
  -H "Content-Type: application/json" \
  -d '{
    "daily_calorie_goal": 2000,
    "daily_protein_goal": 150,
    "daily_carbs_goal": 250,
    "daily_fat_goal": 65
  }' -w "\n%{http_code}\n"

# Invalid update (negative)
curl -b cookies.txt -X POST http://localhost:5000/api/update_goals \
  -H "Content-Type: application/json" \
  -d '{"daily_calorie_goal": -100}' \
  -w "\n%{http_code}\n"
```

Expected:
- Valid: `200 OK`
- Invalid: `400 Bad Request`

---

### Test 8: Authentication Check
**Goal:** Verify protected routes require login

1. Logout from `/logout`
2. Navigate directly to `http://localhost:5000/track`
3. Expected: ❌ Redirect to `/login`
4. Expected status code: `302 Found` (redirect)

5. Try AJAX call without login:
```bash
curl http://localhost:5000/api/profile_data -w "\n%{http_code}\n"
```

Expected response:
```json
{
  "success": false,
  "error": "Not logged in"
}
401
```

---

### Test 9: Error Handling - MongoDB Down
**Goal:** Verify graceful error when MongoDB is offline

1. Stop MongoDB: `Ctrl+C` in MongoDB terminal
2. Navigate to `/track`
3. Expected: ❌ Page still loads (no infinite hang)
4. Expected: Error message shows: "Error loading meals"
5. Wait 5 seconds max (MongoDB timeout)

**Check logs for:**
```
connection timeout after 5 seconds
serverSelectionTimeoutMS exceeded
```

---

### Test 10: Error Handling - Food Not Found
**Goal:** Verify 404 error when food doesn't exist

```bash
curl -b cookies.txt -X POST http://localhost:5000/api/add_food \
  -H "Content-Type: application/json" \
  -d '{"food_id":"nonexistentfood123","quantity":100}' \
  -w "\n%{http_code}\n"
```

Expected response:
```json
{
  "success": false,
  "error": "Food not found"
}
404
```

---

## 🔍 Browser Console Testing

Open browser DevTools (F12) → Network tab and check:

### For successful login:
```
POST /login           200 OK
Response headers include: Set-Cookie
```

### For adding food:
```
POST /api/add_food    200 OK
Response: {"success": true, "message": "..."}
```

### For search:
```
GET /api/search_foods?q=pi    200 OK
Response: [{"id": "...", "name": "Pizza", ...}]
```

### For unauthorized access:
```
GET /api/profile_data         401 Unauthorized
Response: {"success": false, "error": "Not logged in"}
```

---

## 📊 Validation Checklist

Before considering deployment complete:

### Database
- [ ] MongoDB is running
- [ ] Connection timeout is working (5 seconds)
- [ ] Foods database is populated
- [ ] Can create new users

### Authentication
- [ ] Login works with valid credentials
- [ ] Login fails with invalid credentials (401)
- [ ] Signup works with valid data
- [ ] Signup fails with duplicate email (409)
- [ ] Sessions persist after login
- [ ] Logout clears session

### Food Tracking
- [ ] /track page loads (no "Loading..." hang)
- [ ] Search returns results (200 OK)
- [ ] Add food works (200 OK)
- [ ] Remove food works (200 OK)
- [ ] Daily summary updates

### Error Handling
- [ ] Missing fields return 400
- [ ] Unauthorized access returns 401
- [ ] Not found items return 404
- [ ] Database errors return 500 with message
- [ ] All errors display friendly messages

### Performance
- [ ] Pages load within 2 seconds
- [ ] MongoDB connection timeout after 5 seconds
- [ ] No infinite "Loading..." hangs
- [ ] Error pages render gracefully

---

## 🚀 Deployment Steps

### 1. Pre-deployment Testing
```bash
# Run validation script
python validate_system.py

# Check all routes
python test_tracking.py
```

### 2. Check Configuration
```python
# In app.py, ensure:
app.run(debug=False)  # Not debug=True in production
```

### 3. MongoDB Setup
```python
# In database.py, verify:
serverSelectionTimeoutMS=5000
connectTimeoutMS=5000
```

### 4. Session Management
```python
# In app.py, verify:
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.permanent_session_lifetime = timedelta(days=7)
```

### 5. Deploy
```bash
# Using production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🐛 Debugging Commands

### Check Flask Logs
```bash
python app.py 2>&1 | tee flask.log
# Monitor: tail -f flask.log
```

### Test MongoDB Connection
```python
from database import Database
db = Database()
print("✅ Connected" if db.client else "❌ Failed")
```

### Clear Sessions (for testing)
```bash
rm -rf flask_session/*
```

### Reset Database (warning: deletes all data)
```bash
python init_food_database.py
python populate_foods.py
```

---

## 📞 Common Issues & Solutions

### Issue: "Loading..." forever on /track page
**Solution:**
1. Check MongoDB is running: `mongod`
2. Check connection timeout in database.py (should be 5000ms)
3. Restart Flask: `python app.py`
4. Check logs for "connection timeout" message

### Issue: Login fails with 500 error
**Solution:**
1. Check user exists in database
2. Check bcrypt is installed: `pip install bcrypt`
3. Check Flask logs for specific error

### Issue: Search returns 500 error
**Solution:**
1. Check MongoDB is running
2. Check foods collection is populated: `python populate_foods.py`
3. Check database connection has timeout

### Issue: Signup fails with 409 (email exists)
**Solution:**
- This is expected for duplicate emails
- Try different email address

### Issue: Session lost after page refresh
**Solution:**
1. Check `session.permanent = True` in login route
2. Check `app.permanent_session_lifetime` is set
3. Clear browser cookies and try again

---

## 📈 Performance Monitoring

### Check response times
```bash
# Login
time curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass"}'

# Search
time curl "http://localhost:5000/api/search_foods?q=pi"
```

Expected:
- Login: < 500ms
- Search: < 200ms
- Page loads: < 2 seconds

### Monitor database queries
```python
# In database.py, add:
import time
start = time.time()
result = self.db.meals.find(...)
print(f"Query took {time.time() - start:.2f}s")
```

---

## 📚 Additional Resources

- [Flask Error Handling](https://flask.palletsprojects.com/en/2.3.x/errorhandling/)
- [HTTP Status Codes](https://httpwg.org/specs/rfc9110.html#status.codes)
- [MongoDB Connection Strings](https://docs.mongodb.com/manual/reference/connection-string/)
- [RESTful API Best Practices](https://restfulapi.net/)

---

**Status:** ✅ All routes fixed and ready for testing
**Last Updated:** After all 12 routes enhanced
**Test Coverage:** 10 comprehensive test cases provided

