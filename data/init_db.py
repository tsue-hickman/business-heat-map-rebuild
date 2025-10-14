import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Location, Demographic

def init_database():
    """Initialize the database with tables"""
    app = create_app('development')
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if tables are empty
        user_count = User.query.count()
        location_count = Location.query.count()
        demographic_count = Demographic.query.count()
        
        print(f"\nCurrent database status:")
        print(f"  Users: {user_count}")
        print(f"  Locations: {location_count}")
        print(f"  Demographics: {demographic_count}")

if __name__ == '__main__':
    init_database()