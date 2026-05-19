#!/usr/bin/env python3
"""
NutriAI - Smart Meal Planner
Run this script to start the application
"""

import os
import sys
from app import app

def main():
    """Main function to run the Flask application"""
    print("🧠 NutriAI - Smart Meal Planner")
    print("=" * 40)
    print("Starting the application...")
    print("📱 Open your browser and go to: http://127.0.0.1:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        # Run the Flask app
        app.run(
            debug=True,
            host='127.0.0.1',
            port=5000,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n👋 Thanks for using NutriAI!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()