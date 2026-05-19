#!/usr/bin/env python3
"""
Create a test user for nutrition analysis testing
"""
import bcrypt
from database import Database

def create_test_user():
    """Create a test user for testing nutrition analysis"""

    db = Database()

    # Test user data
    email = 'test@example.com'
    password = 'password123'
    first_name = 'Test'
    last_name = 'User'

    # Check if user already exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        print(f"Test user {email} already exists")
        return

    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create user
    try:
        result = db.create_user(email, password_hash, first_name, last_name)
        print(f"✓ Test user created successfully: {email}")
        print(f"Password: {password}")
    except Exception as e:
        print(f"✗ Failed to create test user: {e}")

if __name__ == '__main__':
    create_test_user()