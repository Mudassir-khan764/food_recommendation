# HTTP Status Code Reference - All Endpoints

## Authentication Endpoints

### POST /login
```
✅ 200 OK - Login successful, session established
❌ 400 Bad Request - Missing email or password
❌ 401 Unauthorized - Incorrect credentials
❌ 500 Server Error - Database connection error
```

### POST /signup
```
✅ 200 OK - Account created successfully
❌ 400 Bad Request - Missing required fields or validation failed
❌ 409 Conflict - Email already registered
❌ 500 Server Error - Database error during registration
```

### GET /logout
```
✅ 302 Found - Redirect to login (session cleared)
```

---

## Page Routes (Protected)

### GET /dashboard
```
✅ 200 OK - Dashboard loaded with user data
❌ 302 Found - Redirect to /login if not authenticated
❌ No error on database errors - graceful fallback with flash message
```

### GET /track
```
✅ 200 OK - Track page loaded with today's meals
❌ 302 Found - Redirect to /login if not authenticated
❌ No error on database errors - graceful fallback with flash message
```

### GET /profile
```
✅ 200 OK - Profile page loaded with summary data
❌ 302 Found - Redirect to /login if not authenticated
❌ No error on database errors - graceful fallback with flash message
```

---

## AJAX API Endpoints (Protected)

### POST /api/add_food
```
✅ 200 OK - Food added to meal successfully
❌ 400 Bad Request - Missing food_id or quantity
❌ 401 Unauthorized - Not logged in (session expired)
❌ 404 Not Found - Food not found in database
❌ 500 Server Error - Database operation failed
```

**Request Format:**
```json
{
  "food_id": "pizza",
  "quantity": 100
}
```

**Response Format:**
```json
{
  "success": true,
  "message": "Food added successfully",
  "summary": {
    "calories": 250,
    "protein": 10,
    "carbs": 50,
    "fat": 5
  }
}
```

---

### DELETE /api/remove_food/<food_log_id>
```
✅ 200 OK - Food removed successfully
❌ 400 Bad Request - Invalid food_log_id format
❌ 401 Unauthorized - Not logged in
❌ 404 Not Found - Food log doesn't exist
❌ 500 Server Error - Database deletion failed
```

**Response Format:**
```json
{
  "success": true,
  "message": "Food removed successfully",
  "summary": {
    "calories": 200,
    "protein": 8,
    "carbs": 40,
    "fat": 4
  }
}
```

---

### GET /api/search_foods?q=<query>
```
✅ 200 OK - Search results returned (can be empty array)
❌ 500 Server Error - Database search failed
```

**Response Format (Success):**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "name": "Pizza Slice",
    "calories": 250,
    "protein": 10,
    "carbs": 50,
    "fat": 5,
    "portion_size": 100,
    "portion_unit": "g"
  }
]
```

**Response Format (Error):**
```json
{
  "error": "Search error: connection timeout"
}
```
Status: 500

---

### POST /api/update_goals
```
✅ 200 OK - Goals updated successfully
❌ 400 Bad Request - Invalid JSON or negative values
❌ 401 Unauthorized - Not logged in
❌ 500 Server Error - Database update failed
```

**Request Format:**
```json
{
  "daily_calorie_goal": 2000,
  "daily_protein_goal": 150,
  "daily_carbs_goal": 250,
  "daily_fat_goal": 65
}
```

**Response Format:**
```json
{
  "success": true,
  "message": "Goals updated successfully"
}
```

---

### GET /api/profile_data
```
✅ 200 OK - Profile data returned
❌ 401 Unauthorized - Not logged in
❌ 404 Not Found - User profile not found
❌ 500 Server Error - Database query failed
```

**Response Format (Success):**
```json
{
  "success": true,
  "user_name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15 10:30:00",
  "today_summary": {
    "calories": 1500,
    "protein": 120,
    "carbs": 180,
    "fat": 40
  },
  "today_meals": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "food_name": "Breakfast",
      "portion_size": 200,
      "calories": 500,
      "protein": 40,
      "carbs": 60,
      "fat": 15
    }
  ],
  "daily_goals": {
    "daily_calorie_goal": 2000,
    "daily_protein_goal": 150,
    "daily_carbs_goal": 250,
    "daily_fat_goal": 65
  }
}
```

---

### GET /api/today_meals
```
✅ 200 OK - Today's meals and summary returned
❌ 401 Unauthorized - Not logged in
❌ 500 Server Error - Database query failed
```

**Response Format (Success):**
```json
{
  "success": true,
  "meals": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "food_name": "Breakfast",
      "portion_size": 200,
      "calories": 500,
      "protein": 40,
      "carbs": 60,
      "fat": 15
    }
  ],
  "summary": {
    "calories": 1500,
    "protein": 120,
    "carbs": 180,
    "fat": 40
  }
}
```

---

## Error Response Format

All endpoints follow consistent error response format:

### Authentication Error (401)
```json
{
  "success": false,
  "error": "Not logged in"
}
```

### Validation Error (400)
```json
{
  "success": false,
  "error": "Missing fields: email, password"
}
```

### Not Found Error (404)
```json
{
  "success": false,
  "error": "Food not found in database"
}
```

### Server Error (500)
```json
{
  "success": false,
  "error": "Database connection timeout"
}
```

---

## Status Code Summary Table

| Code | Meaning | Common Causes |
|------|---------|---|
| **200** | Success | Normal successful operation |
| **302** | Redirect | Not authenticated, redirect to login |
| **400** | Bad Request | Invalid input, missing fields, validation failed |
| **401** | Unauthorized | Not logged in, session expired, wrong credentials |
| **404** | Not Found | Resource doesn't exist, food not in database |
| **409** | Conflict | Resource already exists (e.g., duplicate email) |
| **500** | Server Error | Database error, exception, connection timeout |

---

## Frontend Handling Guide

### For fetch() calls in JavaScript:

```javascript
// Check HTTP status code first
if (!response.ok) {
  if (response.status === 401) {
    // Redirect to login
    window.location.href = '/login';
  } else if (response.status === 404) {
    // Show "not found" message
    showError('Item not found');
  } else if (response.status === 500) {
    // Show "server error" message
    showError('Server error, please try again');
  } else {
    // Show generic error
    showError('Operation failed');
  }
  return;
}

// Parse and handle success response
const data = await response.json();
if (data.success === false) {
  showError(data.error);
} else {
  // Handle success
  updateUI(data);
}
```

---

## Testing Status Codes

### Using curl:

```bash
# Test login success (200)
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123"}' \
  -w "\n%{http_code}\n"

# Test missing fields (400)
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{}' \
  -w "\n%{http_code}\n"

# Test unauthorized (401)
curl -X GET http://localhost:5000/api/profile_data \
  -w "\n%{http_code}\n"

# Test not found (404)
curl -X POST http://localhost:5000/api/add_food \
  -H "Content-Type: application/json" \
  -d '{"food_id":"nonexistent","quantity":100}' \
  -w "\n%{http_code}\n"
```

---

## Monitoring & Debugging

### Check Flask logs for errors:
```bash
# Terminal output shows:
# - 200 GET /dashboard
# - 401 POST /api/add_food
# - 500 GET /api/search_foods
```

### MongoDB Connection Monitoring:
```python
# Connection now has 5-second timeout
# Log will show:
# ✅ MongoDB connection successful
# ❌ MongoDB connection failed: timeout after 5 seconds
```

---

## Production Readiness

✅ All endpoints return proper HTTP status codes
✅ All endpoints validate input
✅ All endpoints check authentication (except /login, /signup)
✅ All endpoints have error handling
✅ All error messages are user-friendly
✅ No missing return statements
✅ Database operations are wrapped in try-except
✅ Status codes follow REST conventions

