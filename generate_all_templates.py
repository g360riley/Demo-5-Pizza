"""Complete template generator for Pizza Management System"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'app', 'templates')

templates = {
    'pizzas/index.html': '''{% extends "base.html" %}
{% block title %}Pizzas - Pizza Management System{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1><i class="fas fa-pizza-slice me-2"></i>Pizzas</h1>
    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addPizzaModal">
        <i class="fas fa-plus me-2"></i>Add Pizza
    </button>
</div>
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead>
                <tr><th>ID</th><th>Name</th><th>Size</th><th>Price</th><th>Category</th><th>Available</th><th>Actions</th></tr>
            </thead>
            <tbody>
                {% for pizza in pizzas %}
                <tr>
                    <td>{{ pizza.pizza_id }}</td>
                    <td>{{ pizza.name }}</td>
                    <td>{{ pizza.size }}</td>
                    <td>${{ "%.2f"|format(pizza.base_price) }}</td>
                    <td><span class="badge bg-info">{{ pizza.category }}</span></td>
                    <td>{% if pizza.available %}<i class="fas fa-check text-success"></i>{% else %}<i class="fas fa-times text-danger"></i>{% endif %}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editPizza({{ pizza.pizza_id }})"><i class="fas fa-edit"></i></button>
                        <button class="btn btn-sm btn-danger" onclick="deletePizza({{ pizza.pizza_id }})"><i class="fas fa-trash"></i></button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
<!-- Add Pizza Modal -->
<div class="modal fade" id="addPizzaModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header"><h5 class="modal-title">Add New Pizza</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <form id="addPizzaForm">
                <div class="modal-body">
                    <div class="mb-3"><label>Name</label><input type="text" class="form-control" name="name" required></div>
                    <div class="mb-3"><label>Description</label><textarea class="form-control" name="description" rows="2"></textarea></div>
                    <div class="row">
                        <div class="col-md-6 mb-3"><label>Size</label><select class="form-control" name="size" required><option>Small</option><option>Medium</option><option>Large</option></select></div>
                        <div class="col-md-6 mb-3"><label>Price</label><input type="number" step="0.01" class="form-control" name="base_price" required></div>
                    </div>
                    <div class="mb-3"><label>Category</label><select class="form-control" name="category" required><option>Classic</option><option>Specialty</option><option>Vegetarian</option><option>Premium</option></select></div>
                    <div class="mb-3"><input type="checkbox" name="available" value="true" checked> <label>Available</label></div>
                </div>
                <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button><button type="submit" class="btn btn-primary">Add Pizza</button></div>
            </form>
        </div>
    </div>
</div>
<!-- Edit Pizza Modal -->
<div class="modal fade" id="editPizzaModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header"><h5 class="modal-title">Edit Pizza</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <form id="editPizzaForm">
                <input type="hidden" id="edit_pizza_id">
                <div class="modal-body">
                    <div class="mb-3"><label>Name</label><input type="text" class="form-control" id="edit_name" name="name" required></div>
                    <div class="mb-3"><label>Description</label><textarea class="form-control" id="edit_description" name="description" rows="2"></textarea></div>
                    <div class="row">
                        <div class="col-md-6 mb-3"><label>Size</label><select class="form-control" id="edit_size" name="size" required><option>Small</option><option>Medium</option><option>Large</option></select></div>
                        <div class="col-md-6 mb-3"><label>Price</label><input type="number" step="0.01" class="form-control" id="edit_base_price" name="base_price" required></div>
                    </div>
                    <div class="mb-3"><label>Category</label><select class="form-control" id="edit_category" name="category" required><option>Classic</option><option>Specialty</option><option>Vegetarian</option><option>Premium</option></select></div>
                    <div class="mb-3"><input type="checkbox" id="edit_available" name="available" value="true"> <label>Available</label></div>
                </div>
                <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button><button type="submit" class="btn btn-warning">Update Pizza</button></div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
{% block scripts %}
<script>
$('#addPizzaForm').on('submit', function(e) {
    e.preventDefault();
    $.post("{{ url_for('pizzas.create') }}", $(this).serialize()).done(function(r) { alert(r.message); location.reload(); });
});
function editPizza(id) {
    $.get("{{ url_for('pizzas.get', pizza_id=0) }}".replace('/0', '/' + id)).done(function(r) {
        if (r.success) {
            $('#edit_pizza_id').val(r.pizza.pizza_id);
            $('#edit_name').val(r.pizza.name);
            $('#edit_description').val(r.pizza.description);
            $('#edit_size').val(r.pizza.size);
            $('#edit_base_price').val(r.pizza.base_price);
            $('#edit_category').val(r.pizza.category);
            $('#edit_available').prop('checked', r.pizza.available);
            $('#editPizzaModal').modal('show');
        }
    });
}
$('#editPizzaForm').on('submit', function(e) {
    e.preventDefault();
    const id = $('#edit_pizza_id').val();
    $.post("{{ url_for('pizzas.update', pizza_id=0) }}".replace('/0', '/' + id), $(this).serialize()).done(function(r) { alert(r.message); location.reload(); });
});
function deletePizza(id) {
    if (confirm('Delete this pizza?')) {
        $.post("{{ url_for('pizzas.delete', pizza_id=0) }}".replace('/0', '/' + id)).done(function(r) { alert(r.message); location.reload(); });
    }
}
</script>
{% endblock %}
''',

    'orders/index.html': '''{% extends "base.html" %}
{% block title %}Orders - Pizza Management System{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1><i class="fas fa-shopping-cart me-2"></i>Orders</h1>
    <a href="{{ url_for('orders.new') }}" class="btn btn-primary"><i class="fas fa-plus me-2"></i>New Order</a>
</div>
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead>
                <tr><th>Order #</th><th>Customer</th><th>Employee</th><th>Date</th><th>Total</th><th>Tax</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody>
                {% for order in orders %}
                <tr>
                    <td>#{{ order.order_id }}</td>
                    <td>{{ order.customer_name }}</td>
                    <td>{{ order.employee_name }}</td>
                    <td>{{ order.order_date.strftime('%Y-%m-%d %H:%M') if order.order_date else 'N/A' }}</td>
                    <td>${{ "%.2f"|format(order.total_amount) }}</td>
                    <td>${{ "%.2f"|format(order.tax_amount) }} ({{ "%.1f"|format(order.tax_rate * 100) }}%)</td>
                    <td><span class="badge bg-{% if order.status == 'Completed' %}success{% elif order.status == 'Pending' %}warning{% else %}info{% endif %}">{{ order.status }}</span></td>
                    <td>
                        <a href="{{ url_for('orders.view', order_id=order.order_id) }}" class="btn btn-sm btn-info"><i class="fas fa-eye"></i></a>
                        <button class="btn btn-sm btn-danger" onclick="deleteOrder({{ order.order_id }})"><i class="fas fa-trash"></i></button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
{% block scripts %}
<script>
function deleteOrder(id) {
    if (confirm('Delete this order?')) {
        $.post("{{ url_for('orders.delete', order_id=0) }}".replace('/0', '/' + id)).done(function(r) { alert(r.message); location.reload(); });
    }
}
</script>
{% endblock %}
''',

    'orders/new.html': '''{% extends "base.html" %}
{% block title %}New Order - Pizza Management System{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-plus-circle me-2"></i>Create New Order</h1>
<div class="row">
    <div class="col-md-8">
        <div class="card mb-3">
            <div class="card-header"><h5>Order Details</h5></div>
            <div class="card-body">
                <div class="mb-3"><label>Customer</label><select class="form-control" id="customer_id" required>
                    <option value="">Select Customer...</option>
                    {% for customer in customers %}<option value="{{ customer.customer_id }}">{{ customer.full_name }}</option>{% endfor %}
                </select></div>
                <div class="mb-3"><label>Tax Rate (%)</label><input type="number" step="0.01" class="form-control" id="tax_rate" value="7.00" required></div>
                <div class="mb-3"><label>Notes</label><textarea class="form-control" id="notes" rows="2"></textarea></div>
            </div>
        </div>
        <div class="card">
            <div class="card-header"><h5>Select Pizzas</h5></div>
            <div class="card-body">
                {% for pizza in pizzas %}
                <div class="border-bottom pb-2 mb-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <div><strong>{{ pizza.name }}</strong> ({{ pizza.size }}) - ${{ "%.2f"|format(pizza.base_price) }}</div>
                        <div><button class="btn btn-sm btn-success" onclick="addToOrder({{ pizza.pizza_id }}, '{{ pizza.name }}', '{{ pizza.size }}', {{ pizza.base_price }})">Add</button></div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header"><h5>Order Summary</h5></div>
            <div class="card-body" id="orderSummary"><p class="text-muted">No items added</p></div>
            <div class="card-footer">
                <div class="d-flex justify-content-between mb-2"><strong>Subtotal:</strong><span id="subtotal">$0.00</span></div>
                <div class="d-flex justify-content-between mb-2"><strong>Tax:</strong><span id="tax">$0.00</span></div>
                <hr>
                <div class="d-flex justify-content-between mb-3"><strong>Total:</strong><strong id="total">$0.00</strong></div>
                <button class="btn btn-primary w-100" onclick="submitOrder()">Place Order</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block scripts %}
<script>
let orderItems = [];
function addToOrder(id, name, size, price) {
    const existing = orderItems.find(i => i.pizza_id === id);
    if (existing) { existing.quantity++; } else { orderItems.push({pizza_id: id, name, size, unit_price: price, quantity: 1}); }
    updateSummary();
}
function removeItem(id) { orderItems = orderItems.filter(i => i.pizza_id !== id); updateSummary(); }
function updateSummary() {
    if (orderItems.length === 0) { $('#orderSummary').html('<p class="text-muted">No items</p>'); $('#subtotal,#tax,#total').text('$0.00'); return; }
    let html = '<table class="table table-sm">';
    let subtotal = 0;
    orderItems.forEach(item => {
        const itemTotal = item.quantity * item.unit_price;
        subtotal += itemTotal;
        html += `<tr><td>${item.name} (${item.size})</td><td>${item.quantity}x</td><td>$${itemTotal.toFixed(2)}</td><td><button class="btn btn-sm btn-danger" onclick="removeItem(${item.pizza_id})">×</button></td></tr>`;
    });
    html += '</table>';
    $('#orderSummary').html(html);
    const taxRate = parseFloat($('#tax_rate').val()) / 100;
    const taxAmount = subtotal * taxRate;
    const total = subtotal + taxAmount;
    $('#subtotal').text('$' + subtotal.toFixed(2));
    $('#tax').text('$' + taxAmount.toFixed(2));
    $('#total').text('$' + total.toFixed(2));
}
function submitOrder() {
    if (!$('#customer_id').val()) { alert('Select a customer'); return; }
    if (orderItems.length === 0) { alert('Add items'); return; }
    const data = {
        customer_id: $('#customer_id').val(),
        tax_rate: parseFloat($('#tax_rate').val()) / 100,
        notes: $('#notes').val(),
        items: orderItems
    };
    $.ajax({
        url: "{{ url_for('orders.create') }}",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(r) { alert(r.message); window.location.href = "{{ url_for('orders.index') }}"; },
        error: function() { alert('Error creating order'); }
    });
}
$('#tax_rate').on('input', updateSummary);
</script>
{% endblock %}
''',

    'orders/view.html': '''{% extends "base.html" %}
{% block title %}Order #{{ order.order_id }} - Pizza Management System{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1><i class="fas fa-receipt me-2"></i>Order #{{ order.order_id }}</h1>
    <a href="{{ url_for('orders.index') }}" class="btn btn-secondary">Back to Orders</a>
</div>
<div class="row">
    <div class="col-md-6">
        <div class="card mb-3">
            <div class="card-header"><h5>Order Information</h5></div>
            <div class="card-body">
                <p><strong>Order Date:</strong> {{ order.order_date.strftime('%Y-%m-%d %H:%M') if order.order_date else 'N/A' }}</p>
                <p><strong>Status:</strong> <span class="badge bg-{% if order.status == 'Completed' %}success{% elif order.status == 'Pending' %}warning{% else %}info{% endif %}">{{ order.status }}</span></p>
                <p><strong>Notes:</strong> {{ order.notes or 'N/A' }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card mb-3">
            <div class="card-header"><h5>Payment Details</h5></div>
            <div class="card-body">
                <div class="d-flex justify-content-between mb-2"><strong>Subtotal:</strong><span>${{ "%.2f"|format(order.subtotal) }}</span></div>
                <div class="d-flex justify-content-between mb-2"><strong>Tax ({{ "%.1f"|format(order.tax_rate * 100) }}%):</strong><span>${{ "%.2f"|format(order.tax_amount) }}</span></div>
                <hr>
                <div class="d-flex justify-content-between"><h5>Total:</h5><h5>${{ "%.2f"|format(order.total_amount) }}</h5></div>
            </div>
        </div>
    </div>
</div>
<div class="card">
    <div class="card-header"><h5>Order Items</h5></div>
    <div class="card-body">
        <table class="table">
            <thead><tr><th>Pizza</th><th>Size</th><th>Quantity</th><th>Unit Price</th><th>Subtotal</th></tr></thead>
            <tbody>
                {% for detail in details %}
                <tr>
                    <td>{{ detail.pizza_name }}</td>
                    <td>{{ detail.pizza_size }}</td>
                    <td>{{ detail.quantity }}</td>
                    <td>${{ "%.2f"|format(detail.unit_price) }}</td>
                    <td>${{ "%.2f"|format(detail.subtotal) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
''',

    'employees/index.html': '''{% extends "base.html" %}
{% block title %}Employees - Pizza Management System{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1><i class="fas fa-user-tie me-2"></i>Employees</h1>
    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addEmployeeModal"><i class="fas fa-plus me-2"></i>Add Employee</button>
</div>
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Role</th><th>Hire Date</th><th>Status</th><th>Actions</th></tr></thead>
            <tbody>
                {% for emp in employees %}
                <tr>
                    <td>{{ emp.employee_id }}</td>
                    <td>{{ emp.full_name }}</td>
                    <td>{{ emp.email }}</td>
                    <td>{{ emp.phone }}</td>
                    <td><span class="badge bg-primary">{{ emp.role }}</span></td>
                    <td>{{ emp.hire_date.strftime('%Y-%m-%d') if emp.hire_date else 'N/A' }}</td>
                    <td>{% if emp.active %}<span class="badge bg-success">Active</span>{% else %}<span class="badge bg-danger">Inactive</span>{% endif %}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editEmployee({{ emp.employee_id }})"><i class="fas fa-edit"></i></button>
                        <button class="btn btn-sm btn-danger" onclick="deleteEmployee({{ emp.employee_id }})"><i class="fas fa-trash"></i></button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
<!-- Add Employee Modal -->
<div class="modal fade" id="addEmployeeModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header"><h5 class="modal-title">Add New Employee</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <form id="addEmployeeForm">
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6 mb-3"><label>First Name</label><input type="text" class="form-control" name="first_name" required></div>
                        <div class="col-md-6 mb-3"><label>Last Name</label><input type="text" class="form-control" name="last_name" required></div>
                    </div>
                    <div class="mb-3"><label>Email</label><input type="email" class="form-control" name="email" required></div>
                    <div class="mb-3"><label>Phone</label><input type="tel" class="form-control" name="phone" required></div>
                    <div class="mb-3"><label>Role</label><select class="form-control" name="role" required><option>Manager</option><option>Cashier</option><option>Chef</option><option>Delivery</option></select></div>
                    <div class="mb-3"><label>Hire Date</label><input type="date" class="form-control" name="hire_date" required></div>
                </div>
                <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button><button type="submit" class="btn btn-primary">Add Employee</button></div>
            </form>
        </div>
    </div>
</div>
<!-- Edit Employee Modal -->
<div class="modal fade" id="editEmployeeModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header"><h5 class="modal-title">Edit Employee</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <form id="editEmployeeForm">
                <input type="hidden" id="edit_employee_id">
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6 mb-3"><label>First Name</label><input type="text" class="form-control" id="edit_first_name" name="first_name" required></div>
                        <div class="col-md-6 mb-3"><label>Last Name</label><input type="text" class="form-control" id="edit_last_name" name="last_name" required></div>
                    </div>
                    <div class="mb-3"><label>Email</label><input type="email" class="form-control" id="edit_email" name="email" required></div>
                    <div class="mb-3"><label>Phone</label><input type="tel" class="form-control" id="edit_phone" name="phone" required></div>
                    <div class="mb-3"><label>Role</label><select class="form-control" id="edit_role" name="role" required><option>Manager</option><option>Cashier</option><option>Chef</option><option>Delivery</option></select></div>
                    <div class="mb-3"><input type="checkbox" id="edit_active" name="active" value="true"> <label>Active</label></div>
                </div>
                <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button><button type="submit" class="btn btn-warning">Update Employee</button></div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
{% block scripts %}
<script>
$('#addEmployeeForm').on('submit', function(e) {
    e.preventDefault();
    $.post("{{ url_for('employees.create') }}", $(this).serialize()).done(function(r) { alert(r.message); location.reload(); });
});
function editEmployee(id) {
    $.get("{{ url_for('employees.get', employee_id=0) }}".replace('/0', '/' + id)).done(function(r) {
        if (r.success) {
            $('#edit_employee_id').val(r.employee.employee_id);
            $('#edit_first_name').val(r.employee.first_name);
            $('#edit_last_name').val(r.employee.last_name);
            $('#edit_email').val(r.employee.email);
            $('#edit_phone').val(r.employee.phone);
            $('#edit_role').val(r.employee.role);
            $('#edit_active').prop('checked', r.employee.active);
            $('#editEmployeeModal').modal('show');
        }
    });
}
$('#editEmployeeForm').on('submit', function(e) {
    e.preventDefault();
    const id = $('#edit_employee_id').val();
    $.post("{{ url_for('employees.update', employee_id=0) }}".replace('/0', '/' + id), $(this).serialize()).done(function(r) { alert(r.message); location.reload(); });
});
function deleteEmployee(id) {
    if (confirm('Delete this employee?')) {
        $.post("{{ url_for('employees.delete', employee_id=0) }}".replace('/0', '/' + id)).done(function(r) { alert(r.message); location.reload(); });
    }
}
</script>
{% endblock %}
'''
}

def write_template(path, content):
    full_path = os.path.join(TEMPLATES_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

for path, content in templates.items():
    write_template(path, content)

print("\n✓ All templates created successfully!")
