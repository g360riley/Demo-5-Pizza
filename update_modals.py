"""Update all templates to use proper delete confirmation modals"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'app', 'templates')

# Pizza delete modal update
pizzas_index = os.path.join(TEMPLATES_DIR, 'pizzas', 'index.html')
with open(pizzas_index, 'r', encoding='utf-8') as f:
    content = f.read()

# Update delete button
content = content.replace(
    '<button class="btn btn-sm btn-danger" onclick="deletePizza({{ pizza.pizza_id }})"><i class="fas fa-trash"></i></button>',
    '<button class="btn btn-sm btn-danger" onclick="confirmDeletePizza({{ pizza.pizza_id }}, \'{{ pizza.name }} ({{ pizza.size }})\')"><i class="fas fa-trash"></i></button>'
)

# Add delete modal before {% endblock %}
delete_modal = '''
<!-- Delete Confirmation Modal -->
<div class="modal fade" id="deletePizzaModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title"><i class="fas fa-exclamation-triangle me-2"></i>Confirm Delete</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete this pizza?</p>
                <p class="fw-bold" id="deletePizzaName"></p>
                <p class="text-muted mb-0">This action cannot be undone.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" id="confirmDeletePizzaBtn">Delete Pizza</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block scripts %}'''

content = content.replace('{% endblock %}\n{% block scripts %}', delete_modal)

# Update delete function
old_delete = '''function deletePizza(id) {
    if (confirm('Delete this pizza?')) {
        $.post("{{ url_for('pizzas.delete', pizza_id=0) }}".replace('/0', '/' + id)).done(function(r) { alert(r.message); location.reload(); });
    }
}'''

new_delete = '''let deletePizzaId = null;

function confirmDeletePizza(id, name) {
    deletePizzaId = id;
    $('#deletePizzaName').text(name);
    $('#deletePizzaModal').modal('show');
}

$('#confirmDeletePizzaBtn').on('click', function() {
    if (deletePizzaId) {
        $.post("{{ url_for('pizzas.delete', pizza_id=0) }}".replace('/0', '/' + deletePizzaId))
            .done(function(r) {
                $('#deletePizzaModal').modal('hide');
                alert(r.message);
                location.reload();
            });
    }
});'''

content = content.replace(old_delete, new_delete)

with open(pizzas_index, 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ Updated pizzas/index.html")

# Employees delete modal update
employees_index = os.path.join(TEMPLATES_DIR, 'employees', 'index.html')
with open(employees_index, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<button class="btn btn-sm btn-danger" onclick="deleteEmployee({{ emp.employee_id }})"><i class="fas fa-trash"></i></button>',
    '<button class="btn btn-sm btn-danger" onclick="confirmDeleteEmployee({{ emp.employee_id }}, \'{{ emp.full_name }}\')"><i class="fas fa-trash"></i></button>'
)

delete_modal_emp = '''
<!-- Delete Confirmation Modal -->
<div class="modal fade" id="deleteEmployeeModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title"><i class="fas fa-exclamation-triangle me-2"></i>Confirm Delete</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete this employee?</p>
                <p class="fw-bold" id="deleteEmployeeName"></p>
                <p class="text-muted mb-0">This action cannot be undone.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteEmployeeBtn">Delete Employee</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block scripts %}'''

content = content.replace('{% endblock %}\n{% block scripts %}', delete_modal_emp)

old_delete_emp = '''function deleteEmployee(id) {
    if (confirm('Delete this employee?')) {
        $.post("{{ url_for('employees.delete', employee_id=0) }}".replace('/0', '/' + id)).done(function(r) { alert(r.message); location.reload(); });
    }
}'''

new_delete_emp = '''let deleteEmployeeId = null;

function confirmDeleteEmployee(id, name) {
    deleteEmployeeId = id;
    $('#deleteEmployeeName').text(name);
    $('#deleteEmployeeModal').modal('show');
}

$('#confirmDeleteEmployeeBtn').on('click', function() {
    if (deleteEmployeeId) {
        $.post("{{ url_for('employees.delete', employee_id=0) }}".replace('/0', '/' + deleteEmployeeId))
            .done(function(r) {
                $('#deleteEmployeeModal').modal('hide');
                alert(r.message);
                location.reload();
            });
    }
});'''

content = content.replace(old_delete_emp, new_delete_emp)

with open(employees_index, 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ Updated employees/index.html")

# Orders delete modal update
orders_index = os.path.join(TEMPLATES_DIR, 'orders', 'index.html')
with open(orders_index, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<button class="btn btn-sm btn-danger" onclick="deleteOrder({{ order.order_id }})"><i class="fas fa-trash"></i></button>',
    '<button class="btn btn-sm btn-danger" onclick="confirmDeleteOrder({{ order.order_id }}, {{ order.order_id }})"><i class="fas fa-trash"></i></button>'
)

delete_modal_order = '''
<!-- Delete Confirmation Modal -->
<div class="modal fade" id="deleteOrderModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title"><i class="fas fa-exclamation-triangle me-2"></i>Confirm Delete</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete this order?</p>
                <p class="fw-bold">Order #<span id="deleteOrderId"></span></p>
                <p class="text-muted mb-0">This will also delete all associated order details. This action cannot be undone.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteOrderBtn">Delete Order</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block scripts %}'''

content = content.replace('{% endblock %}\n{% block scripts %}', delete_modal_order)

old_delete_order = '''function deleteOrder(id) {
    if (confirm('Delete this order?')) {
        $.post("{{ url_for('orders.delete', order_id=0) }}".replace('/0', '/' + id)).done(function(r) { alert(r.message); location.reload(); });
    }
}'''

new_delete_order = '''let deleteOrderIdValue = null;

function confirmDeleteOrder(id, orderNum) {
    deleteOrderIdValue = id;
    $('#deleteOrderId').text(orderNum);
    $('#deleteOrderModal').modal('show');
}

$('#confirmDeleteOrderBtn').on('click', function() {
    if (deleteOrderIdValue) {
        $.post("{{ url_for('orders.delete', order_id=0) }}".replace('/0', '/' + deleteOrderIdValue))
            .done(function(r) {
                $('#deleteOrderModal').modal('hide');
                alert(r.message);
                location.reload();
            });
    }
});'''

content = content.replace(old_delete_order, new_delete_order)

with open(orders_index, 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ Updated orders/index.html")

print("\nAll templates updated with delete confirmation modals!")
