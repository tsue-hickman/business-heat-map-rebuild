import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extensions import db
from app.models import User, Location, Demographic

def init_database():
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
        
        user_count = User.query.count()
        location_count = Location.query.count()
        demographic_count = Demographic.query.count()
        
        print(f"\nCurrent database status:")
        print(f"  Users: {user_count}")
        print(f"  Locations: {location_count}")
        print(f"  Demographics: {demographic_count}")

if __name__ == '__main__':
    init_database()