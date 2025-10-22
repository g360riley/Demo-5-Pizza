from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Employee(UserMixin):
    """Employee model for authentication and management"""

    def __init__(self, employee_id, first_name, last_name, email, phone, role, password_hash=None, hire_date=None, active=True):
        self.id = employee_id
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.role = role
        self.password_hash = password_hash
        self.hire_date = hire_date
        self.active = active

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Required by Flask-Login"""
        return str(self.employee_id)

    @property
    def is_active(self):
        """Required by Flask-Login"""
        return self.active

    @property
    def full_name(self):
        """Return the employee's full name"""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'


class Customer:
    """Customer model"""

    def __init__(self, customer_id, first_name, last_name, email, phone, address, city, state, zip_code, created_at=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.created_at = created_at

    @property
    def full_name(self):
        """Return the customer's full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def full_address(self):
        """Return the customer's full address"""
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"

    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'


class Pizza:
    """Pizza model"""

    def __init__(self, pizza_id, name, description, size, base_price, category, available=True, created_at=None):
        self.pizza_id = pizza_id
        self.name = name
        self.description = description
        self.size = size
        self.base_price = float(base_price)
        self.category = category
        self.available = available
        self.created_at = created_at

    def __repr__(self):
        return f'<Pizza {self.name} ({self.size})>'


class Order:
    """Order model"""

    def __init__(self, order_id, customer_id, employee_id, order_date, subtotal, tax_rate, tax_amount, total_amount, status, notes=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.order_date = order_date
        self.subtotal = float(subtotal)
        self.tax_rate = float(tax_rate)
        self.tax_amount = float(tax_amount)
        self.total_amount = float(total_amount)
        self.status = status
        self.notes = notes

    def calculate_tax(self):
        """Calculate tax amount based on subtotal and tax rate"""
        self.tax_amount = round(self.subtotal * self.tax_rate, 2)
        return self.tax_amount

    def calculate_total(self):
        """Calculate total amount including tax"""
        self.total_amount = round(self.subtotal + self.tax_amount, 2)
        return self.total_amount

    def __repr__(self):
        return f'<Order #{self.order_id} - ${self.total_amount}>'


class OrderDetail:
    """Order Detail model - represents individual pizzas in an order"""

    def __init__(self, detail_id, order_id, pizza_id, quantity, unit_price, subtotal):
        self.detail_id = detail_id
        self.order_id = order_id
        self.pizza_id = pizza_id
        self.quantity = int(quantity)
        self.unit_price = float(unit_price)
        self.subtotal = float(subtotal)

    def calculate_subtotal(self):
        """Calculate subtotal for this line item"""
        self.subtotal = round(self.quantity * self.unit_price, 2)
        return self.subtotal

    def __repr__(self):
        return f'<OrderDetail Order#{self.order_id} - {self.quantity}x Pizza#{self.pizza_id}>'
