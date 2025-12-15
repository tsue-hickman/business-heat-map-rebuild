import os
from flask import Flask
from app.extensions import db, login_manager

def create_app(config_name='development'):
    """Create Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-please-change')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///business_heatmap.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import and register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.admin import admin
    
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Create tables in app context
    with app.app_context():
        # Import all models to ensure they're registered
        from app.models import User, Location, Demographic, SearchHistory, SavedAddress
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)