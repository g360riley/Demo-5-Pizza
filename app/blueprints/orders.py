from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.db_service import (
    get_all_orders, get_order_by_id, get_order_details,
    create_order, update_order_status, delete_order,
    get_all_customers, get_available_pizzas
)

orders = Blueprint('orders', __name__)

@orders.route('/')
@login_required
def index():
    """List all orders"""
    order_list = get_all_orders()
    return render_template('orders/index.html', orders=order_list)

@orders.route('/new')
@login_required
def new():
    """Create new order form"""
    customers = get_all_customers()
    pizzas = get_available_pizzas()
    return render_template('orders/new.html', customers=customers, pizzas=pizzas)

@orders.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new order via AJAX"""
    try:
        data = request.get_json()
        customer_id = int(data['customer_id'])
        employee_id = current_user.employee_id
        tax_rate = float(data.get('tax_rate', 0.0700))
        notes = data.get('notes', '')

        # Parse order items: list of {pizza_id, quantity, unit_price}
        order_items = []
        for item in data['items']:
            pizza_id = int(item['pizza_id'])
            quantity = int(item['quantity'])
            unit_price = float(item['unit_price'])
            order_items.append((pizza_id, quantity, unit_price))

        order_id = create_order(customer_id, employee_id, order_items, tax_rate, notes)

        if order_id:
            return jsonify({'success': True, 'message': 'Order created successfully!', 'order_id': order_id})
        else:
            return jsonify({'success': False, 'message': 'Failed to create order.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders.route('/view/<int:order_id>')
@login_required
def view(order_id):
    """View order details"""
    order = get_order_by_id(order_id)
    if not order:
        return "Order not found", 404

    details = get_order_details(order_id)
    return render_template('orders/view.html', order=order, details=details)

@orders.route('/details/<int:order_id>')
@login_required
def get_details(order_id):
    """Get order details via AJAX"""
    order = get_order_by_id(order_id)
    if not order:
        return jsonify({'success': False, 'message': 'Order not found.'}), 404

    details = get_order_details(order_id)

    return jsonify({
        'success': True,
        'order': {
            'order_id': order.order_id,
            'customer_id': order.customer_id,
            'employee_id': order.employee_id,
            'order_date': order.order_date.isoformat() if order.order_date else None,
            'subtotal': float(order.subtotal),
            'tax_rate': float(order.tax_rate),
            'tax_amount': float(order.tax_amount),
            'total_amount': float(order.total_amount),
            'status': order.status,
            'notes': order.notes
        },
        'details': [{
            'detail_id': d.detail_id,
            'pizza_id': d.pizza_id,
            'pizza_name': d.pizza_name,
            'pizza_size': d.pizza_size,
            'quantity': d.quantity,
            'unit_price': float(d.unit_price),
            'subtotal': float(d.subtotal)
        } for d in details]
    })

@orders.route('/update-status/<int:order_id>', methods=['POST'])
@login_required
def update_status(order_id):
    """Update order status via AJAX"""
    try:
        data = request.form
        status = data['status']
        success = update_order_status(order_id, status)

        if success:
            return jsonify({'success': True, 'message': 'Order status updated successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update order status.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@orders.route('/delete/<int:order_id>', methods=['POST'])
@login_required
def delete(order_id):
    """Delete an order via AJAX"""
    try:
        success = delete_order(order_id)
        if success:
            return jsonify({'success': True, 'message': 'Order deleted successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete order.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
