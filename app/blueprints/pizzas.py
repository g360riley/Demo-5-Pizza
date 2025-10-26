from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.db_service import (
    get_all_pizzas, get_pizza_by_id, get_archived_pizzas,
    create_pizza, update_pizza, delete_pizza,
    restore_pizza, permanently_delete_pizza
)

pizzas = Blueprint('pizzas', __name__)

@pizzas.route('/')
@login_required
def index():
    """List all pizzas"""
    pizza_list = get_all_pizzas()
    return render_template('pizzas/index.html', pizzas=pizza_list)

@pizzas.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new pizza via AJAX"""
    try:
        data = request.form
        available = data.get('available', 'true').lower() == 'true'
        pizza_id = create_pizza(
            data['name'],
            data['description'],
            data['size'],
            float(data['base_price']),
            data['category'],
            available
        )
        if pizza_id:
            return jsonify({'success': True, 'message': 'Pizza created successfully!', 'pizza_id': pizza_id})
        else:
            return jsonify({'success': False, 'message': 'Failed to create pizza.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@pizzas.route('/get/<int:pizza_id>')
@login_required
def get(pizza_id):
    """Get pizza details via AJAX"""
    pizza = get_pizza_by_id(pizza_id)
    if pizza:
        return jsonify({
            'success': True,
            'pizza': {
                'pizza_id': pizza.pizza_id,
                'name': pizza.name,
                'description': pizza.description,
                'size': pizza.size,
                'base_price': pizza.base_price,
                'category': pizza.category,
                'available': pizza.available
            }
        })
    return jsonify({'success': False, 'message': 'Pizza not found.'}), 404

@pizzas.route('/update/<int:pizza_id>', methods=['POST'])
@login_required
def update(pizza_id):
    """Update a pizza via AJAX"""
    try:
        data = request.form
        available = data.get('available', 'true').lower() == 'true'
        success = update_pizza(
            pizza_id,
            data['name'],
            data['description'],
            data['size'],
            float(data['base_price']),
            data['category'],
            available
        )
        if success:
            return jsonify({'success': True, 'message': 'Pizza updated successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update pizza.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@pizzas.route('/delete/<int:pizza_id>', methods=['POST'])
@login_required
def delete(pizza_id):
    """Archive a pizza via AJAX"""
    try:
        success = delete_pizza(pizza_id)
        if success:
            return jsonify({'success': True, 'message': 'Pizza archived successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to archive pizza.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@pizzas.route('/archived')
@login_required
def archived():
    """List all archived pizzas"""
    pizza_list = get_archived_pizzas()
    return render_template('pizzas/index.html', pizzas=pizza_list, show_archived=True)

@pizzas.route('/restore/<int:pizza_id>', methods=['POST'])
@login_required
def restore(pizza_id):
    """Restore an archived pizza via AJAX"""
    try:
        success = restore_pizza(pizza_id)
        if success:
            return jsonify({'success': True, 'message': 'Pizza restored successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to restore pizza.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@pizzas.route('/permanent-delete/<int:pizza_id>', methods=['POST'])
@login_required
def permanent_delete(pizza_id):
    """Permanently delete a pizza via AJAX"""
    try:
        success = permanently_delete_pizza(pizza_id)
        if success:
            return jsonify({'success': True, 'message': 'Pizza permanently deleted!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete pizza.'}), 500
    except Exception as e:
        error_msg = str(e)
        if 'foreign key constraint' in error_msg.lower() or 'cannot delete' in error_msg.lower():
            return jsonify({'success': False, 'message': 'Cannot delete pizza: it is referenced in existing orders. You can only archive it.'}), 400
        return jsonify({'success': False, 'message': f'Error: {error_msg}'}), 500
