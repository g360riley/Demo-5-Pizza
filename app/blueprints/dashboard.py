from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.db_service import get_dashboard_stats

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    """Dashboard home with sales metrics"""
    stats = get_dashboard_stats()
    return render_template('dashboard/index.html', stats=stats, current_user=current_user)
