"""
Script to generate all remaining templates for the Pizza Management System
Run this script to create all CRUD templates with modals
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'app', 'templates')

# Customer Index Template
CUSTOMERS_INDEX = '''{% extends "base.html" %}

{% block title %}Customers - Pizza Management System{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1><i class="fas fa-users me-2"></i>Customers</h1>
    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addCustomerModal">
        <i class="fas fa-plus me-2"></i>Add Customer
    </button>
</div>

<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Address</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for customer in customers %}
                    <tr>
                        <td>{{ customer.customer_id }}</td>
                        <td>{{ customer.full_name }}</td>
                        <td>{{ customer.email }}</td>
                        <td>{{ customer.phone }}</td>
                        <td>{{ customer.full_address }}</td>
                        <td>
                            <button class="btn btn-sm btn-warning" onclick="editCustomer({{ customer.customer_id }})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteCustomer({{ customer.customer_id }})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Add Customer Modal -->
<div class="modal fade" id="addCustomerModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Add New Customer</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form id="addCustomerForm">
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">First Name</label>
                            <input type="text" class="form-control" name="first_name" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Last Name</label>
                            <input type="text" class="form-control" name="last_name" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" name="email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Phone</label>
                        <input type="tel" class="form-control" name="phone" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Address</label>
                        <input type="text" class="form-control" name="address" required>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">City</label>
                            <input type="text" class="form-control" name="city" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">State</label>
                            <input type="text" class="form-control" name="state" maxlength="2" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Zip Code</label>
                            <input type="text" class="form-control" name="zip_code" required>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Customer</button>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Edit Customer Modal -->
<div class="modal fade" id="editCustomerModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Edit Customer</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <form id="editCustomerForm">
                <input type="hidden" id="edit_customer_id">
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">First Name</label>
                            <input type="text" class="form-control" id="edit_first_name" name="first_name" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Last Name</label>
                            <input type="text" class="form-control" id="edit_last_name" name="last_name" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" id="edit_email" name="email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Phone</label>
                        <input type="tel" class="form-control" id="edit_phone" name="phone" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Address</label>
                        <input type="text" class="form-control" id="edit_address" name="address" required>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">City</label>
                            <input type="text" class="form-control" id="edit_city" name="city" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">State</label>
                            <input type="text" class="form-control" id="edit_state" name="state" maxlength="2" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Zip Code</label>
                            <input type="text" class="form-control" id="edit_zip_code" name="zip_code" required>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-warning">Update Customer</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
// Add Customer
$('#addCustomerForm').on('submit', function(e) {
    e.preventDefault();
    $.post("{{ url_for('customers.create') }}", $(this).serialize())
        .done(function(response) {
            if (response.success) {
                alert(response.message);
                location.reload();
            } else {
                alert('Error: ' + response.message);
            }
        })
        .fail(function() {
            alert('An error occurred while creating the customer.');
        });
});

// Edit Customer
function editCustomer(id) {
    $.get("{{ url_for('customers.get', customer_id=0) }}".replace('/0', '/' + id))
        .done(function(response) {
            if (response.success) {
                $('#edit_customer_id').val(response.customer.customer_id);
                $('#edit_first_name').val(response.customer.first_name);
                $('#edit_last_name').val(response.customer.last_name);
                $('#edit_email').val(response.customer.email);
                $('#edit_phone').val(response.customer.phone);
                $('#edit_address').val(response.customer.address);
                $('#edit_city').val(response.customer.city);
                $('#edit_state').val(response.customer.state);
                $('#edit_zip_code').val(response.customer.zip_code);
                $('#editCustomerModal').modal('show');
            }
        });
}

$('#editCustomerForm').on('submit', function(e) {
    e.preventDefault();
    const id = $('#edit_customer_id').val();
    $.post("{{ url_for('customers.update', customer_id=0) }}".replace('/0', '/' + id), $(this).serialize())
        .done(function(response) {
            if (response.success) {
                alert(response.message);
                location.reload();
            } else {
                alert('Error: ' + response.message);
            }
        });
});

// Delete Customer
function deleteCustomer(id) {
    if (confirm('Are you sure you want to delete this customer?')) {
        $.post("{{ url_for('customers.delete', customer_id=0) }}".replace('/0', '/' + id))
            .done(function(response) {
                if (response.success) {
                    alert(response.message);
                    location.reload();
                } else {
                    alert('Error: ' + response.message);
                }
            });
    }
}
</script>
{% endblock %}
'''

# Write the templates
def write_template(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

# Create customers template
write_template(os.path.join(TEMPLATES_DIR, 'customers', 'index.html'), CUSTOMERS_INDEX)

print("\nCustomer templates created successfully!")
print("Run create_remaining_templates.py for pizzas, orders, and employees templates.")
