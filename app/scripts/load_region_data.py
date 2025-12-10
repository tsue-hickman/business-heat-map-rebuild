# app/scripts/load_region_data.py
# This script loads demographic data for the ZIP codes you specified
# Atlantic Iowa, St. Joseph Missouri, and Leavenworth Kansas regions

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.extensions import db
from app.models import Demographic

def load_regional_data():
    """Load sample demographic data for your target regions"""
    
    # Import create_app
    import importlib.util
    spec = importlib.util.spec_from_file_location("app", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    app = app_module.create_app('development')
    
    with app.app_context():
        print("Loading regional demographic data...")
        
        # Sample data for key cities in your regions
        # In a real app, you'd fetch this from Census API
        regional_data = [
            # Atlantic Iowa Region
            {
                'zip_code': '50022',
                'city': 'Anita',
                'state': 'IA',
                'population': 973,
                'median_income': 42500,
                'median_age': 44.2,
                'median_home_value': 68900,
                'households': 428
            },
            {
                'zip_code': '50025',
                'city': 'Atlantic',
                'state': 'IA',
                'population': 6792,
                'median_income': 45800,
                'median_age': 41.8,
                'median_home_value': 89700,
                'households': 2934
            },
            {
                'zip_code': '51520',
                'city': 'Council Bluffs',
                'state': 'IA',
                'population': 62230,
                'median_income': 48900,
                'median_age': 37.2,
                'median_home_value': 125600,
                'households': 25100
            },
            {
                'zip_code': '51601',
                'city': 'Shenandoah',
                'state': 'IA',
                'population': 5048,
                'median_income': 46200,
                'median_age': 42.5,
                'median_home_value': 82400,
                'households': 2234
            },
            
            # St. Joseph Missouri Region
            {
                'zip_code': '64501',
                'city': 'Saint Joseph',
                'state': 'MO',
                'population': 76780,
                'median_income': 44100,
                'median_age': 36.8,
                'median_home_value': 112300,
                'households': 31200
            },
            {
                'zip_code': '64503',
                'city': 'Saint Joseph',
                'state': 'MO',
                'population': 22450,
                'median_income': 52300,
                'median_age': 39.4,
                'median_home_value': 138900,
                'households': 9100
            },
            
            # Leavenworth Kansas Region
            {
                'zip_code': '66027',
                'city': 'Leavenworth',
                'state': 'KS',
                'population': 35290,
                'median_income': 51200,
                'median_age': 32.4,
                'median_home_value': 142600,
                'households': 13500
            },
            {
                'zip_code': '66048',
                'city': 'Leavenworth',
                'state': 'KS',
                'population': 8920,
                'median_income': 48700,
                'median_age': 35.2,
                'median_home_value': 128400,
                'households': 3240
            },
            {
                'zip_code': '66002',
                'city': 'Atchison',
                'state': 'KS',
                'population': 10960,
                'median_income': 43800,
                'median_age': 38.9,
                'median_home_value': 89200,
                'households': 4520
            },
            
            # Kansas City Metro (for context)
            {
                'zip_code': '64101',
                'city': 'Kansas City',
                'state': 'MO',
                'population': 8450,
                'median_income': 52000,
                'median_age': 34.5,
                'median_home_value': 185000,
                'households': 3200
            },
            {
                'zip_code': '66207',
                'city': 'Overland Park',
                'state': 'KS',
                'population': 15600,
                'median_income': 78000,
                'median_age': 42.1,
                'median_home_value': 295000,
                'households': 5800
            },
        ]
        
        # Add each demographic record
        added_count = 0
        updated_count = 0
        
        for data in regional_data:
            # Check if this ZIP already exists
            existing = Demographic.query.filter_by(zip_code=data['zip_code']).first()
            
            if existing:
                # Update existing record
                existing.city = data['city']
                existing.state = data['state']
                existing.population = data['population']
                existing.median_income = data['median_income']
                existing.median_age = data['median_age']
                existing.median_home_value = data['median_home_value']
                existing.households = data['households']
                updated_count += 1
                print(f"Updated: {data['zip_code']} - {data['city']}, {data['state']}")
            else:
                # Create new record
                demo = Demographic(**data)
                db.session.add(demo)
                added_count += 1
                print(f"Added: {data['zip_code']} - {data['city']}, {data['state']}")
        
        # Save all changes
        db.session.commit()
        
        print(f"\n✅ Successfully loaded regional data!")
        print(f"   Added: {added_count} new ZIP codes")
        print(f"   Updated: {updated_count} existing ZIP codes")
        print(f"   Total demographics in database: {Demographic.query.count()}")
        
        print("\n💡 Tip: View these on your heat map at http://localhost:5000/map")

if __name__ == '__main__':
    load_regional_data()