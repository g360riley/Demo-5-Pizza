from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from app.db_service import (
    get_all_customers, get_customer_by_id,
    create_customer, update_customer, delete_customer
)

customers = Blueprint('customers', __name__)

@customers.route('/')
@login_required
def index():
    """List all customers"""
    customer_list = get_all_customers()
    return render_template('customers/index.html', customers=customer_list)

@customers.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new customer via AJAX"""
    try:
        data = request.form
        customer_id = create_customer(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone'],
            data['address'],
            data['city'],
            data['state'],
            data['zip_code']
        )
        if customer_id:
            return jsonify({'success': True, 'message': 'Customer created successfully!', 'customer_id': customer_id})
        else:
            return jsonify({'success': False, 'message': 'Failed to create customer.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@customers.route('/get/<int:customer_id>')
@login_required
def get(customer_id):
    """Get customer details via AJAX"""
    customer = get_customer_by_id(customer_id)
    if customer:
        return jsonify({
            'success': True,
            'customer': {
                'customer_id': customer.customer_id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'phone': customer.phone,
                'address': customer.address,
                'city': customer.city,
                'state': customer.state,
                'zip_code': customer.zip_code
            }
        })
    return jsonify({'success': False, 'message': 'Customer not found.'}), 404

@customers.route('/update/<int:customer_id>', methods=['POST'])
@login_required
def update(customer_id):
    """Update a customer via AJAX"""
    try:
        data = request.form
        success = update_customer(
            customer_id,
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone'],
            data['address'],
            data['city'],
            data['state'],
            data['zip_code']
        )
        if success:
            return jsonify({'success': True, 'message': 'Customer updated successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update customer.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@customers.route('/delete/<int:customer_id>', methods=['POST'])
@login_required
def delete(customer_id):
    """Archive a customer via AJAX"""
    try:
        success = delete_customer(customer_id)
        if success:
            return jsonify({'success': True, 'message': 'Customer archived successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to archive customer.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
