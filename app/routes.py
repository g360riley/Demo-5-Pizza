from flask import render_template, redirect, url_for
from flask_login import current_user
from . import app

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@app.route('/about')
def about():
    return render_template('about.html')
