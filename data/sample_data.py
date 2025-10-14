import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extensions import db
from app.models import User, Location, Demographic

def load_sample_data():
    # Import create_app from the root app.py
    import importlib.util
    spec = importlib.util.spec_from_file_location("app", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    app = app_module.create_app('development')
    
    with app.app_context():
        print("Loading sample data...")
        
        if User.query.count() > 0:
            print("⚠️  Database already has data. Skipping...")
            return
        
        admin = User(
            username='admin',
            email='admin@businessheatmap.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        user = User(
            username='demo_user',
            email='demo@businessheatmap.com',
            role='user'
        )
        user.set_password('demo123')
        db.session.add(user)
        
        db.session.commit()
        print("✅ Created 2 sample users")
        
        locations = [
            Location(
                name='Downtown Coffee Shop',
                address='123 Main St',
                city='Kansas City',
                state='MO',
                zip_code='64101',
                latitude=39.0997,
                longitude=-94.5786,
                business_type='Coffee Shop',
                notes='Prime downtown location',
                created_by=admin.id
            ),
            Location(
                name='Suburban Fitness Center',
                address='456 Oak Avenue',
                city='Overland Park',
                state='KS',
                zip_code='66207',
                latitude=38.9822,
                longitude=-94.6708,
                business_type='Fitness',
                notes='Growing suburban area',
                created_by=admin.id
            ),
            Location(
                name='Plaza Restaurant',
                address='789 Ward Parkway',
                city='Kansas City',
                state='MO',
                zip_code='64112',
                latitude=39.0399,
                longitude=-94.5919,
                business_type='Restaurant',
                notes='Country Club Plaza district',
                created_by=user.id
            )
        ]
        
        db.session.add_all(locations)
        db.session.commit()
        print(f"✅ Created {len(locations)} sample locations")
        
        demographics = [
            Demographic(
                zip_code='64101',
                city='Kansas City',
                state='MO',
                population=8450,
                median_income=52000,
                median_age=34.5,
                median_home_value=185000,
                households=3200
            ),
            Demographic(
                zip_code='66207',
                city='Overland Park',
                state='KS',
                population=15600,
                median_income=78000,
                median_age=42.1,
                median_home_value=295000,
                households=5800
            ),
            Demographic(
                zip_code='64112',
                city='Kansas City',
                state='MO',
                population=12300,
                median_income=95000,
                median_age=38.7,
                median_home_value=385000,
                households=4900
            ),
            Demographic(
                zip_code='64030',
                city='Grandview',
                state='MO',
                population=9200,
                median_income=45000,
                median_age=31.2,
                median_home_value=145000,
                households=3400
            )
        ]
        
        db.session.add_all(demographics)
        db.session.commit()
        print(f"✅ Created {len(demographics)} demographic records")
        
        print("\n🎉 Sample data loaded successfully!")
        print("\nLogin credentials:")
        print("  Admin: username='admin', password='admin123'")
        print("  User:  username='demo_user', password='demo123'")

if __name__ == '__main__':
    load_sample_data()