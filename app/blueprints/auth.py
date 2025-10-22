from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.db_service import get_employee_by_email, update_employee, update_employee_password

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Employee login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        employee = get_employee_by_email(email)

        if employee and employee.check_password(password):
            if not employee.active:
                flash('Your account has been deactivated. Please contact your manager.', 'error')
                return redirect(url_for('auth.login'))

            login_user(employee, remember=remember)
            flash(f'Welcome back, {employee.first_name}!', 'success')

            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('auth/login.html')

@auth.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html')

@auth.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # Check if email is already taken by another user
    existing_employee = get_employee_by_email(email)
    if existing_employee and existing_employee.employee_id != current_user.employee_id:
        flash('This email is already in use by another employee.', 'error')
        return redirect(url_for('auth.profile'))

    # Update employee (keeping role and active status the same)
    success = update_employee(
        current_user.employee_id,
        first_name,
        last_name,
        email,
        phone,
        current_user.role,
        current_user.active
    )

    if success:
        # Update current_user object attributes
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        current_user.phone = phone
        flash('Profile updated successfully!', 'success')
    else:
        flash('Failed to update profile. Please try again.', 'error')

    return redirect(url_for('auth.profile'))

@auth.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Verify current password
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('auth.profile'))

    # Check if new passwords match
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('auth.profile'))

    # Check minimum password length
    if len(new_password) < 6:
        flash('Password must be at least 6 characters long.', 'error')
        return redirect(url_for('auth.profile'))

    # Update password
    current_user.set_password(new_password)
    success = update_employee_password(current_user.employee_id, current_user.password_hash)

    if success:
        flash('Password changed successfully!', 'success')
    else:
        flash('Failed to change password. Please try again.', 'error')

    return redirect(url_for('auth.profile'))

@auth.route('/logout')
@login_required
def logout():
    """Employee logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))
