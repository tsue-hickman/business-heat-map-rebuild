# app/routes/main.py
# Main routes for the application - these handle different pages/URLs

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Location, Demographic
from app.extensions import db

# Blueprint is like a mini-app that groups related routes together
bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    """Homepage - shows project status"""
    return render_template('index.html')

@bp.route('/dashboard')
@login_required  # This decorator means you must be logged in to access
def dashboard():
    """User dashboard - shows your locations and stats"""
    # Query the database for locations created by current user
    user_locations = Location.query.filter_by(created_by=current_user.id).all()
    
    # Get total counts for stats display
    total_users = User.query.count()
    total_locations = Location.query.count()
    total_demographics = Demographic.query.count()
    
    # render_template fills in the HTML template with this data
    return render_template('dashboard.html',
                         user_locations=user_locations,
                         total_users=total_users,
                         total_locations=total_locations,
                         total_demographics=total_demographics)

# ============ API ENDPOINTS ============
# These return JSON data (not HTML pages) for JavaScript to use

@bp.route('/api/stats')
def stats():
    """API endpoint that returns database statistics as JSON"""
    try:
        user_count = User.query.count()
        location_count = Location.query.count()
        demographic_count = Demographic.query.count()
        
        return jsonify({
            'status': 'success',
            'database': 'connected',
            'stats': {
                'users': user_count,
                'locations': location_count,
                'demographics': demographic_count
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/locations')
def get_locations():
    """Get all business locations as JSON"""
    try:
        locations = Location.query.all()
        return jsonify({
            'status': 'success',
            'count': len(locations),
            'locations': [{
                'id': loc.id,
                'name': loc.name,
                'address': loc.address,
                'city': loc.city,
                'state': loc.state,
                'zip_code': loc.zip_code,
                'latitude': loc.latitude,
                'longitude': loc.longitude,
                'business_type': loc.business_type
            } for loc in locations]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/demographics')
def get_demographics():
    """Get all demographic data as JSON"""
    try:
        demographics = Demographic.query.all()
        return jsonify({
            'status': 'success',
            'count': len(demographics),
            'demographics': [{
                'zip_code': demo.zip_code,
                'city': demo.city,
                'state': demo.state,
                'population': demo.population,
                'median_income': demo.median_income,
                'income_range': demo.get_income_range(),
                'median_home_value': demo.median_home_value,
                'median_age': demo.median_age,
                'households': demo.households
            } for demo in demographics]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ============ ADD LOCATION FEATURE ============

@bp.route('/add-location', methods=['GET', 'POST'])
@login_required
def add_location():
    """Page to add a new business location"""
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        business_type = request.form.get('business_type')
        notes = request.form.get('notes')
        
        # Basic validation
        if not all([name, address, city, state, zip_code]):
            flash('Please fill out all required fields.', 'danger')
            return render_template('add_location.html')
        
        # Try to get latitude/longitude if provided
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        # Convert to float if they exist, otherwise None
        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except ValueError:
            latitude = None
            longitude = None
        
        # Create new location object
        new_location = Location(
            name=name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            latitude=latitude,
            longitude=longitude,
            business_type=business_type if business_type else None,
            notes=notes,
            created_by=current_user.id
        )
        
        # Save to database
        try:
            db.session.add(new_location)
            db.session.commit()
            flash(f'Successfully added {name}!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding location: {str(e)}', 'danger')
    
    # If GET request, just show the form
    return render_template('add_location.html')

@bp.route('/map')
def map_view():
    """Interactive heat map page"""
    return render_template('map.html')

# Helper route for testing
@bp.route('/hello')
def hello():
    return jsonify({
        'message': 'Flask app is working!',
        'status': 'success'
    })