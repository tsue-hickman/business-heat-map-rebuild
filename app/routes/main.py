from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import User, Location, Demographic
from app.extensions import db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - requires login"""
    # Get user's locations
    user_locations = Location.query.filter_by(created_by=current_user.id).all()
    
    # Get total counts
    total_users = User.query.count()
    total_locations = Location.query.count()
    total_demographics = Demographic.query.count()
    
    return render_template('dashboard.html',
                         user_locations=user_locations,
                         total_users=total_users,
                         total_locations=total_locations,
                         total_demographics=total_demographics)

@bp.route('/hello')
def hello():
    return jsonify({
        'message': 'Flask app is working!',
        'status': 'success'
    })

@bp.route('/api/stats')
def stats():
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
                'median_home_value': demo.median_home_value
            } for demo in demographics]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500