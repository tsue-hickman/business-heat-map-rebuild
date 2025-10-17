from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app.models import User, Location, Demographic
from app.extensions import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def panel():
    """Admin panel - only accessible by admins"""
    users = User.query.all()
    locations = Location.query.all()
    demographics = Demographic.query.all()
    
    # Get some statistics
    total_users = len(users)
    total_admins = sum(1 for u in users if u.is_admin())
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

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    """Manage all users"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@bp.route('/locations')
@login_required
@admin_required
def manage_locations():
    """Manage all locations"""
    locations = Location.query.order_by(Location.created_at.desc()).all()
    return render_template('admin/locations.html', locations=locations)

@bp.route('/demographics')
@login_required
@admin_required
def manage_demographics():
    """Manage demographic data"""
    demographics = Demographic.query.order_by(Demographic.zip_code).all()
    return render_template('admin/demographics.html', demographics=demographics)