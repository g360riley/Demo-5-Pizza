from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.db_service import (
    get_all_employees, get_employee_by_id,
    create_employee, update_employee, delete_employee
)

employees = Blueprint('employees', __name__)

@employees.route('/')
@login_required
def index():
    """List all employees"""
    employee_list = get_all_employees()
    return render_template('employees/index.html', employees=employee_list)

@employees.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new employee via AJAX"""
    try:
        data = request.form
        employee_id = create_employee(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone'],
            data['role'],
            data.get('password', 'password123'),  # Default password
            data['hire_date']
        )
        if employee_id:
            return jsonify({'success': True, 'message': 'Employee created successfully!', 'employee_id': employee_id})
        else:
            return jsonify({'success': False, 'message': 'Failed to create employee.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@employees.route('/get/<int:employee_id>')
@login_required
def get(employee_id):
    """Get employee details via AJAX"""
    employee = get_employee_by_id(employee_id)
    if employee:
        return jsonify({
            'success': True,
            'employee': {
                'employee_id': employee.employee_id,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'email': employee.email,
                'phone': employee.phone,
                'role': employee.role,
                'hire_date': employee.hire_date.isoformat() if employee.hire_date else None,
                'active': employee.active
            }
        })
    return jsonify({'success': False, 'message': 'Employee not found.'}), 404

@employees.route('/update/<int:employee_id>', methods=['POST'])
@login_required
def update(employee_id):
    """Update an employee via AJAX"""
    try:
        data = request.form
        active = data.get('active', 'true').lower() == 'true'
        success = update_employee(
            employee_id,
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone'],
            data['role'],
            active
        )
        if success:
            return jsonify({'success': True, 'message': 'Employee updated successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update employee.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@employees.route('/delete/<int:employee_id>', methods=['POST'])
@login_required
def delete(employee_id):
    """Delete an employee via AJAX"""
    try:
        success = delete_employee(employee_id)
        if success:
            return jsonify({'success': True, 'message': 'Employee deleted successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete employee.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
