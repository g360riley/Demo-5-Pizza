from flask import Flask, g, session
from flask_login import LoginManager, current_user
from .app_factory import create_app
from .db_connect import close_db, get_db
import os

app = create_app()
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from app.db_service import get_employee_by_id
    return get_employee_by_id(int(user_id))

# Register Blueprints
from app.blueprints.examples import examples
from app.blueprints.auth import auth
from app.blueprints.dashboard import dashboard
from app.blueprints.customers import customers
from app.blueprints.pizzas import pizzas
from app.blueprints.orders import orders
from app.blueprints.employees import employees

app.register_blueprint(examples, url_prefix='/example')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(customers, url_prefix='/customers')
app.register_blueprint(pizzas, url_prefix='/pizzas')
app.register_blueprint(orders, url_prefix='/orders')
app.register_blueprint(employees, url_prefix='/employees')

from . import routes

@app.before_request
def before_request():
    g.db = get_db()
    if g.db is None:
        print("Warning: Database connection unavailable. Some features may not work.")

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)

# Add cache-control headers to prevent browser caching of protected pages
@app.after_request
def add_security_headers(response):
    """Add security headers to prevent caching of authenticated pages"""
    # Only add no-cache headers for authenticated users or protected routes
    if current_user.is_authenticated:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

    return response