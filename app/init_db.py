# app/init_db.py
# This script creates all the database tables
# Run it once to set up your database

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extensions import db
from app.models import User, Location, Demographic

def init_database():
    """Create all database tables"""
    # Import create_app from the root app.py
    import importlib.util
    spec = importlib.util.spec_from_file_location("app", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    app = app_module.create_app('development')
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Show current counts
        user_count = User.query.count()
        location_count = Location.query.count()
        demographic_count = Demographic.query.count()
        
        print(f"\nCurrent database status:")
        print(f"  Users: {user_count}")
        print(f"  Locations: {location_count}")
        print(f"  Demographics: {demographic_count}")

if __name__ == '__main__':
    init_database()