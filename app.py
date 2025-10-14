from flask import Flask
from flask_login import LoginManager
from app.extensions import db
import os

# Initialize login manager
login_manager = LoginManager()

def create_app(config_name='development'):
    app = Flask(__name__, 
                template_folder='app/templates',
                static_folder='app/static')
    
    from config import config
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # User loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import models and create tables
    with app.app_context():
        from app.models import User, Location, Demographic
        db.create_all()
    
    # Import and register blueprints
    from app.routes import main, auth, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000, debug=True)