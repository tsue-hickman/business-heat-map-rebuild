from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Demographic, Location, User, SearchHistory, SavedAddress
from datetime import datetime

main = Blueprint('main', __name__)

# ============= PAGE ROUTES =============

@main.route('/')
def index():
    """Redirect to map if logged in, otherwise show login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.map_view'))
    return redirect(url_for('auth.login'))

@main.route('/map')
@login_required
def map_view():
    """Main map interface"""
    return render_template('map.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        current_user.phone = request.form.get('phone')
        
        # Handle password change
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password:
            if new_password != confirm_password:
                flash('Passwords do not match!', 'error')
                return redirect(url_for('main.profile'))
            
            if current_password:
                from werkzeug.security import check_password_hash, generate_password_hash
                if check_password_hash(current_user.password_hash, current_password):
                    current_user.password_hash = generate_password_hash(new_password)
                else:
                    flash('Current password is incorrect!', 'error')
                    return redirect(url_for('main.profile'))
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html')

@main.route('/search-history')
@login_required
def search_history_page():
    """Search history page"""
    return render_template('search_history.html')

@main.route('/saved-addresses')
@login_required
def saved_addresses_page():
    """Saved addresses page"""
    return render_template('saved_addresses.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - redirect to map"""
    return redirect(url_for('main.map_view'))


# ============= API ENDPOINTS =============

@main.route('/api/demographics')
def api_demographics():
    """Get all demographics data"""
    demographics = Demographic.query.all()
    
    result = []
    for demo in demographics:
        # Determine income range
        if demo.median_income:
            if demo.median_income < 40000:
                income_range = 'Low Income'
            elif demo.median_income < 75000:
                income_range = 'Middle Income'
            elif demo.median_income < 120000:
                income_range = 'Upper Middle'
            else:
                income_range = 'High Income'
        else:
            income_range = 'Unknown'
        
        result.append({
            'id': demo.id,
            'zip_code': demo.zip_code,
            'city': demo.city,
            'state': demo.state,
            'population': demo.population,
            'median_income': demo.median_income,
            'median_age': demo.median_age,
            'median_home_value': demo.median_home_value,
            'households': demo.households,
            'income_range': income_range
        })
    
    return jsonify({
        'demographics': result,
        'count': len(result)
    })

@main.route('/api/locations')
def api_locations():
    """Get all business locations"""
    if current_user.is_authenticated and current_user.is_admin:
        locations = Location.query.all()
    elif current_user.is_authenticated:
        locations = Location.query.filter_by(user_id=current_user.id).all()
    else:
        locations = []
    
    return jsonify({
        'locations': [loc.to_dict() for loc in locations],
        'count': len(locations)
    })


# ============= SEARCH HISTORY API =============

@main.route('/api/search-history', methods=['GET', 'POST'])
@login_required
def api_search_history():
    """Save and retrieve search history"""
    if request.method == 'POST':
        data = request.json
        
        search = SearchHistory(
            user_id=current_user.id,
            zip_code=data.get('zip_code'),
            filters=data.get('filters', {})
        )
        db.session.add(search)
        db.session.commit()
        
        return jsonify({'success': True, 'id': search.id})
    
    # GET request - retrieve history
    searches = SearchHistory.query.filter_by(user_id=current_user.id)\
        .order_by(SearchHistory.search_date.desc())\
        .limit(20).all()
    
    return jsonify({
        'searches': [s.to_dict() for s in searches]
    })


# ============= SAVED ADDRESSES API =============

@main.route('/api/saved-addresses', methods=['GET', 'POST'])
@login_required
def api_saved_addresses():
    """Get or create saved addresses"""
    if request.method == 'POST':
        data = request.json
        
        address = SavedAddress(
            user_id=current_user.id,
            name=data.get('name'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            address_type=data.get('address_type', 'residential'),
            filters_used=data.get('filters_used'),
            notes=data.get('notes')
        )
        db.session.add(address)
        db.session.commit()
        
        return jsonify({'success': True, 'id': address.id})
    
    # GET request
    addresses = SavedAddress.query.filter_by(user_id=current_user.id)\
        .order_by(SavedAddress.created_at.desc()).all()
    
    return jsonify({
        'addresses': [addr.to_dict() for addr in addresses]
    })

@main.route('/api/saved-addresses/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_saved_address_detail(id):
    """Update or delete a saved address"""
    address = SavedAddress.query.get_or_404(id)
    
    # Check ownership
    if address.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'PUT':
        data = request.json
        address.name = data.get('name', address.name)
        address.notes = data.get('notes', address.notes)
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        db.session.delete(address)
        db.session.commit()
        return jsonify({'success': True})


# ============= ADMIN API =============

@main.route('/api/admin/stats')
@login_required
def api_admin_stats():
    """Get admin statistics"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'users': User.query.count(),
        'locations': Location.query.count(),
        'demographics': Demographic.query.count(),
        'saved_addresses': SavedAddress.query.count()
    })


# ============= OLD ROUTES (Keep for backward compatibility) =============

@main.route('/add-location', methods=['GET', 'POST'])
@login_required
def add_location():
    """Add a new business location"""
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        business_type = request.form.get('business_type')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        location = Location(
            name=name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            business_type=business_type,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            user_id=current_user.id
        )
        
        db.session.add(location)
        db.session.commit()
        
        flash('Location added successfully!', 'success')
        return redirect(url_for('main.map_view'))
    
    # GET - show form
    demographics = Demographic.query.all()
    return render_template('add_location.html', demographics=demographics)


# Error handlers
@main.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500