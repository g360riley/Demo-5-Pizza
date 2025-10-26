"""
Database service layer for Pizza Management System
Handles all database operations using the models
"""

from flask import g
from app.models import Employee, Customer, Pizza, Order, OrderDetail
from app.db_connect import get_db

# ==================== EMPLOYEE OPERATIONS ====================

def get_employee_by_id(employee_id):
    """Get employee by ID"""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    cursor.execute("""
        SELECT employee_id, first_name, last_name, email, phone, role,
               password_hash, hire_date, active
        FROM employees WHERE employee_id = %s
    """, (employee_id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        return Employee(**row)
    return None

def get_employee_by_email(email):
    """Get employee by email"""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    cursor.execute("""
        SELECT employee_id, first_name, last_name, email, phone, role,
               password_hash, hire_date, active
        FROM employees WHERE email = %s
    """, (email,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        return Employee(**row)
    return None

def get_all_employees():
    """Get all employees"""
    db = get_db()
    if not db:
        return []

    cursor = db.cursor()
    cursor.execute("""
        SELECT employee_id, first_name, last_name, email, phone, role,
               password_hash, hire_date, active
        FROM employees ORDER BY last_name, first_name
    """)
    rows = cursor.fetchall()
    cursor.close()

    return [Employee(**row) for row in rows]

def create_employee(first_name, last_name, email, phone, role, password, hire_date):
    """Create a new employee"""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    employee = Employee(None, first_name, last_name, email, phone, role, hire_date=hire_date)
    employee.set_password(password)

    cursor.execute("""
        INSERT INTO employees (first_name, last_name, email, phone, role, password_hash, hire_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (first_name, last_name, email, phone, role, employee.password_hash, hire_date))
    db.commit()

    employee_id = cursor.lastrowid
    cursor.close()
    return employee_id

def update_employee(employee_id, first_name, last_name, email, phone, role, active):
    """Update an employee"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("""
        UPDATE employees
        SET first_name = %s, last_name = %s, email = %s, phone = %s, role = %s, active = %s
        WHERE employee_id = %s
    """, (first_name, last_name, email, phone, role, active, employee_id))
    db.commit()
    cursor.close()
    return True

def delete_employee(employee_id):
    """Delete an employee"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    db.commit()
    cursor.close()
    return True

def update_employee_password(employee_id, password_hash):
    """Update employee password"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("""
        UPDATE employees
        SET password_hash = %s
        WHERE employee_id = %s
    """, (password_hash, employee_id))
    db.commit()
    cursor.close()
    return True

# ==================== CUSTOMER OPERATIONS ====================

def get_all_customers():
    """Get all non-archived customers"""
    db = get_db()
    if not db:
        return []

    cursor = db.cursor()
    cursor.execute("""
        SELECT customer_id, first_name, last_name, email, phone,
               address, city, state, zip_code, created_at
        FROM customers WHERE archived = FALSE ORDER BY last_name, first_name
    """)
    rows = cursor.fetchall()
    cursor.close()

    return [Customer(**row) for row in rows]

def get_customer_by_id(customer_id):
    """Get customer by ID"""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    cursor.execute("""
        SELECT customer_id, first_name, last_name, email, phone,
               address, city, state, zip_code, created_at
        FROM customers WHERE customer_id = %s
    """, (customer_id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        return Customer(**row)
    return None

def create_customer(first_name, last_name, email, phone, address, city, state, zip_code):
    """Create a new customer"""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (first_name, last_name, email, phone, address, city, state, zip_code))
    db.commit()

    customer_id = cursor.lastrowid
    cursor.close()
    return customer_id

def update_customer(customer_id, first_name, last_name, email, phone, address, city, state, zip_code):
    """Update a customer"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("""
        UPDATE customers
        SET first_name = %s, last_name = %s, email = %s, phone = %s,
            address = %s, city = %s, state = %s, zip_code = %s
        WHERE customer_id = %s
    """, (first_name, last_name, email, phone, address, city, state, zip_code, customer_id))
    db.commit()
    cursor.close()
    return True

def delete_customer(customer_id):
    """Archive a customer (soft delete to preserve order history)"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("UPDATE customers SET archived = TRUE WHERE customer_id = %s", (customer_id,))
    db.commit()
    cursor.close()
    return True

# ==================== PIZZA OPERATIONS ====================

def get_all_pizzas():
    """Get all non-archived pizzas"""
    db = get_db()
    if not db:
        return []

    cursor = db.cursor()
    cursor.execute("""
        SELECT pizza_id, name, description, size, base_price, category, available, created_at
        FROM pizzas WHERE archived = FALSE ORDER BY category, name, size
    """)
    rows = cursor.fetchall()
    cursor.close()

    return [Pizza(**row) for row in rows]

def get_available_pizzas():
    """Get all available non-archived pizzas"""
    db = get_db()
    if not db:
        return []

    cursor = db.cursor()
    cursor.execute("""
        SELECT pizza_id, name, description, size, base_price, category, available, created_at
        FROM pizzas WHERE available = TRUE AND archived = FALSE ORDER BY category, name, size
    """)
    rows = cursor.fetchall()
    cursor.close()

    return [Pizza(**row) for row in rows]

def get_pizza_by_id(pizza_id):
    """Get pizza by ID"""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    cursor.execute("""
        SELECT pizza_id, name, description, size, base_price, category, available, created_at
        FROM pizzas WHERE pizza_id = %s
    """, (pizza_id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        return Pizza(**row)
    return None

def create_pizza(name, description, size, base_price, category, available=True):
    """Create a new pizza"""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO pizzas (name, description, size, base_price, category, available)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, description, size, base_price, category, available))
    db.commit()

    pizza_id = cursor.lastrowid
    cursor.close()
    return pizza_id

def update_pizza(pizza_id, name, description, size, base_price, category, available):
    """Update a pizza"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("""
        UPDATE pizzas
        SET name = %s, description = %s, size = %s, base_price = %s,
            category = %s, available = %s
        WHERE pizza_id = %s
    """, (name, description, size, base_price, category, available, pizza_id))
    db.commit()
    cursor.close()
    return True

def delete_pizza(pizza_id):
    """Archive a pizza (soft delete to preserve sales data)"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("UPDATE pizzas SET archived = TRUE WHERE pizza_id = %s", (pizza_id,))
    db.commit()
    cursor.close()
    return True

def get_archived_pizzas():
    """Get all archived pizzas"""
    db = get_db()
    if not db:
        return []

    cursor = db.cursor()
    cursor.execute("""
        SELECT pizza_id, name, description, size, base_price, category, available, created_at
        FROM pizzas WHERE archived = TRUE ORDER BY category, name, size
    """)
    rows = cursor.fetchall()
    cursor.close()

    return [Pizza(**row) for row in rows]

def restore_pizza(pizza_id):
    """Restore an archived pizza (unarchive)"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("UPDATE pizzas SET archived = FALSE WHERE pizza_id = %s", (pizza_id,))
    db.commit()
    cursor.close()
    return True

def permanently_delete_pizza(pizza_id):
    """Permanently delete a pizza from the database"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    # This will fail if pizza is referenced in orders due to foreign key constraint
    try:
        cursor.execute("DELETE FROM pizzas WHERE pizza_id = %s", (pizza_id,))
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        db.rollback()
        cursor.close()
        raise e

# ==================== ORDER OPERATIONS ====================

def get_all_orders():
    """Get all orders with customer and employee information"""
    db = get_db()
    if not db:
        return []

    cursor = db.cursor()
    cursor.execute("""
        SELECT o.order_id, o.customer_id, o.employee_id, o.order_date,
               o.subtotal, o.tax_rate, o.tax_amount, o.total_amount, o.status, o.notes,
               c.first_name as customer_first_name, c.last_name as customer_last_name,
               e.first_name as employee_first_name, e.last_name as employee_last_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN employees e ON o.employee_id = e.employee_id
        ORDER BY o.order_date DESC
    """)
    rows = cursor.fetchall()
    cursor.close()

    orders = []
    for row in rows:
        order = Order(
            row['order_id'], row['customer_id'], row['employee_id'],
            row['order_date'], row['subtotal'], row['tax_rate'],
            row['tax_amount'], row['total_amount'], row['status'], row['notes']
        )
        order.customer_name = f"{row['customer_first_name']} {row['customer_last_name']}"
        order.employee_name = f"{row['employee_first_name']} {row['employee_last_name']}"
        orders.append(order)

    return orders

def get_order_by_id(order_id):
    """Get order by ID"""
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()
    cursor.execute("""
        SELECT order_id, customer_id, employee_id, order_date,
               subtotal, tax_rate, tax_amount, total_amount, status, notes
        FROM orders WHERE order_id = %s
    """, (order_id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        return Order(**row)
    return None

def get_order_details(order_id):
    """Get all order details for a specific order"""
    db = get_db()
    if not db:
        return []

    cursor = db.cursor()
    cursor.execute("""
        SELECT od.detail_id, od.order_id, od.pizza_id, od.quantity,
               od.unit_price, od.subtotal,
               p.name as pizza_name, p.size as pizza_size
        FROM order_details od
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        WHERE od.order_id = %s
    """, (order_id,))
    rows = cursor.fetchall()
    cursor.close()

    details = []
    for row in rows:
        detail = OrderDetail(
            row['detail_id'], row['order_id'], row['pizza_id'],
            row['quantity'], row['unit_price'], row['subtotal']
        )
        detail.pizza_name = row['pizza_name']
        detail.pizza_size = row['pizza_size']
        details.append(detail)

    return details

def create_order(customer_id, employee_id, order_items, tax_rate=0.0700, notes=None):
    """
    Create a new order with order details
    order_items: list of tuples (pizza_id, quantity, unit_price)
    """
    db = get_db()
    if not db:
        return None

    cursor = db.cursor()

    # Calculate subtotal
    subtotal = sum(item[1] * item[2] for item in order_items)
    tax_amount = round(subtotal * tax_rate, 2)
    total_amount = round(subtotal + tax_amount, 2)

    # Create order
    cursor.execute("""
        INSERT INTO orders (customer_id, employee_id, subtotal, tax_rate, tax_amount, total_amount, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (customer_id, employee_id, subtotal, tax_rate, tax_amount, total_amount, 'Pending', notes))

    order_id = cursor.lastrowid

    # Create order details
    for pizza_id, quantity, unit_price in order_items:
        item_subtotal = round(quantity * unit_price, 2)
        cursor.execute("""
            INSERT INTO order_details (order_id, pizza_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, pizza_id, quantity, unit_price, item_subtotal))

    db.commit()
    cursor.close()
    return order_id

def update_order_status(order_id, status):
    """Update order status"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("""
        UPDATE orders SET status = %s WHERE order_id = %s
    """, (status, order_id))
    db.commit()
    cursor.close()
    return True

def delete_order(order_id):
    """Delete an order (and its details due to CASCADE)"""
    db = get_db()
    if not db:
        return False

    cursor = db.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    db.commit()
    cursor.close()
    return True

# ==================== DASHBOARD ANALYTICS ====================

def get_dashboard_stats():
    """Get dashboard statistics"""
    db = get_db()
    if not db:
        return {}

    cursor = db.cursor()

    # Total sales
    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total_sales FROM orders")
    total_sales = cursor.fetchone()['total_sales']

    # Total orders
    cursor.execute("SELECT COUNT(*) as total_orders FROM orders")
    total_orders = cursor.fetchone()['total_orders']

    # Total customers
    cursor.execute("SELECT COUNT(*) as total_customers FROM customers")
    total_customers = cursor.fetchone()['total_customers']

    # Pending orders
    cursor.execute("SELECT COUNT(*) as pending_orders FROM orders WHERE status = 'Pending'")
    pending_orders = cursor.fetchone()['pending_orders']

    # Recent orders (last 5)
    cursor.execute("""
        SELECT o.order_id, o.order_date, o.total_amount, o.status,
               c.first_name, c.last_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
        LIMIT 5
    """)
    recent_orders = cursor.fetchall()

    # Top selling pizzas
    cursor.execute("""
        SELECT p.name, p.size, SUM(od.quantity) as total_sold
        FROM order_details od
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        GROUP BY p.pizza_id, p.name, p.size
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    top_pizzas = cursor.fetchall()

    # Sales by status
    cursor.execute("""
        SELECT status, COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total
        FROM orders
        GROUP BY status
    """)
    sales_by_status = cursor.fetchall()

    cursor.close()

    return {
        'total_sales': float(total_sales),
        'total_orders': total_orders,
        'total_customers': total_customers,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'top_pizzas': top_pizzas,
        'sales_by_status': sales_by_status
    }
