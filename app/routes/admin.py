from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app.models import User, Location, Demographic
from app.extensions import db

# Changed from 'bp' to 'admin' and removed url_prefix (it's in app/__init__.py)
admin = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        # is_admin is a PROPERTY not a method - no ()
        if not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('main.map_view'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def panel():
    """Admin panel - only accessible by admins"""
    users = User.query.all()
    locations = Location.query.all()
    demographics = Demographic.query.all()
    
    # Get statistics - is_admin is a boolean field, not a method
    total_users = len(users)
    total_admins = sum(1 for u in users if u.is_admin)
    total_locations = len(locations)
    total_demographics = len(demographics)
    
    return render_template('admin/panel.html',
                         users=users,
                         locations=locations,
                         demographics=demographics,
                         total_users=total_users,
                         total_admins=total_admins,
                         total_locations=total_locations,
                         total_demographics=total_demographics)

@admin.route('/users')
@login_required
@admin_required
def manage_users():
    """Manage all users"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin.route('/locations')
@login_required
@admin_required
def manage_locations():
    """Manage all locations"""
    locations = Location.query.order_by(Location.created_at.desc()).all()
    return render_template('admin/locations.html', locations=locations)

@admin.route('/demographics')
@login_required
@admin_required
def manage_demographics():
    """Manage demographic data"""
    demographics = Demographic.query.order_by(Demographic.zip_code).all()
    return render_template('admin/demographics.html', demographics=demographics)