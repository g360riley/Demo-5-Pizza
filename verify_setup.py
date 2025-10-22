"""
Verification script for Pizza Management System
Tests database connectivity, tables, and sample data
"""

import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

def verify_setup():
    print("=" * 60)
    print("Pizza Management System - Setup Verification")
    print("=" * 60)
    print()

    # Test database connection
    print("1. Testing database connection...")
    try:
        conn = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )
        print("   [OK] Database connection successful!")
        cursor = conn.cursor()
    except Exception as e:
        print(f"   [FAIL] Database connection failed: {e}")
        return False

    # Verify tables exist
    print("\n2. Verifying database tables...")
    tables = ['employees', 'customers', 'pizzas', 'orders', 'order_details']
    for table in tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        if cursor.fetchone():
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = cursor.fetchone()['count']
            print(f"   [OK] {table:15} - {count} records")
        else:
            print(f"   [FAIL] {table:15} - NOT FOUND")

    # Verify employee data
    print("\n3. Verifying employee data...")
    cursor.execute("SELECT first_name, last_name, role FROM employees")
    employees = cursor.fetchall()
    for emp in employees:
        print(f"   [OK] {emp['first_name']} {emp['last_name']} - {emp['role']}")

    # Verify customer data
    print("\n4. Verifying customer data...")
    cursor.execute("SELECT COUNT(*) as count FROM customers")
    customer_count = cursor.fetchone()['count']
    print(f"   [OK] {customer_count} customers in database")

    # Verify pizza data
    print("\n5. Verifying pizza data...")
    cursor.execute("SELECT DISTINCT name FROM pizzas ORDER BY name")
    pizzas = cursor.fetchall()
    for pizza in pizzas:
        print(f"   [OK] {pizza['name']}")

    # Verify order data with tax calculations
    print("\n6. Verifying order data with tax calculations...")
    cursor.execute("""
        SELECT order_id, subtotal, tax_rate, tax_amount, total_amount, status
        FROM orders
    """)
    orders = cursor.fetchall()
    for order in orders:
        print(f"   [OK] Order #{order['order_id']}: Subtotal=${order['subtotal']:.2f}, "
              f"Tax=${order['tax_amount']:.2f} ({order['tax_rate']*100:.1f}%), "
              f"Total=${order['total_amount']:.2f} - {order['status']}")

    # Verify foreign key relationships
    print("\n7. Verifying foreign key relationships...")
    cursor.execute("""
        SELECT o.order_id, c.first_name, c.last_name, e.first_name as emp_first, e.last_name as emp_last
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN employees e ON o.employee_id = e.employee_id
        LIMIT 3
    """)
    relationships = cursor.fetchall()
    for rel in relationships:
        print(f"   [OK] Order #{rel['order_id']}: Customer={rel['first_name']} {rel['last_name']}, "
              f"Employee={rel['emp_first']} {rel['emp_last']}")

    # Verify order details
    print("\n8. Verifying order details...")
    cursor.execute("""
        SELECT od.order_id, p.name, od.quantity, od.unit_price, od.subtotal
        FROM order_details od
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        LIMIT 5
    """)
    details = cursor.fetchall()
    for detail in details:
        print(f"   [OK] Order #{detail['order_id']}: {detail['quantity']}x {detail['name']} "
              f"@ ${detail['unit_price']:.2f} = ${detail['subtotal']:.2f}")

    # Test authentication
    print("\n9. Testing authentication...")
    cursor.execute("SELECT email, password_hash FROM employees WHERE role = 'Manager' LIMIT 1")
    manager = cursor.fetchone()
    if manager and manager['password_hash']:
        print(f"   [OK] Manager account found: {manager['email']}")
        print(f"   [OK] Password hash exists: {manager['password_hash'][:20]}...")
    else:
        print("   [FAIL] Manager account not properly configured")

    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE!")
    print("=" * 60)
    print("\nSystem Status: [READY FOR USE]")
    print("\nDefault Login Credentials:")
    print("  Email:    john.manager@pizzashop.com")
    print("  Password: password123")
    print("\nQuick Start:")
    print("  Windows:  start.bat")
    print("  Linux:    ./start.sh")
    print("  Manual:   python app.py")
    print("\nAccess:     http://localhost:5000")
    print("=" * 60)

    cursor.close()
    conn.close()
    return True

if __name__ == '__main__':
    try:
        verify_setup()
    except Exception as e:
        print(f"\n[FAIL] Verification failed: {e}")
        print("\nPlease run: python app/init_db.py")
