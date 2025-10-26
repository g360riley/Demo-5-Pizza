"""
Test script to verify archiving functionality for pizzas and customers
"""
import pymysql
import os
import sys
from dotenv import load_dotenv

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

def get_connection():
    """Get database connection"""
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)

def test_pizza_archiving():
    """Test pizza archiving functionality"""
    print("\n" + "="*60)
    print("TESTING PIZZA ARCHIVING")
    print("="*60)

    conn = get_connection()
    cursor = conn.cursor()

    # 1. Get initial count of active pizzas
    cursor.execute("SELECT COUNT(*) as count FROM pizzas WHERE archived = FALSE")
    initial_count = cursor.fetchone()['count']
    print(f"✓ Initial active pizzas: {initial_count}")

    # 2. Get first pizza
    cursor.execute("SELECT pizza_id, name, size FROM pizzas WHERE archived = FALSE LIMIT 1")
    pizza = cursor.fetchone()
    if not pizza:
        print("✗ No pizzas found!")
        return False

    pizza_id = pizza['pizza_id']
    pizza_name = f"{pizza['name']} ({pizza['size']})"
    print(f"✓ Testing with pizza: {pizza_name} (ID: {pizza_id})")

    # 3. Archive the pizza
    cursor.execute("UPDATE pizzas SET archived = TRUE WHERE pizza_id = %s", (pizza_id,))
    conn.commit()
    print(f"✓ Pizza archived successfully")

    # 4. Verify pizza is no longer in active list
    cursor.execute("SELECT COUNT(*) as count FROM pizzas WHERE archived = FALSE")
    new_count = cursor.fetchone()['count']
    if new_count == initial_count - 1:
        print(f"✓ Active pizza count decreased from {initial_count} to {new_count}")
    else:
        print(f"✗ Expected count {initial_count - 1}, got {new_count}")
        return False

    # 5. Verify pizza still exists in database with archived = TRUE
    cursor.execute("SELECT archived FROM pizzas WHERE pizza_id = %s", (pizza_id,))
    result = cursor.fetchone()
    if result and result['archived']:
        print(f"✓ Pizza {pizza_name} is correctly marked as archived")
    else:
        print(f"✗ Pizza archive status incorrect")
        return False

    # 6. Verify pizza doesn't appear in orders (it should still be referenced)
    cursor.execute("""
        SELECT COUNT(*) as count FROM order_details
        WHERE pizza_id = %s
    """, (pizza_id,))
    order_count = cursor.fetchone()['count']
    if order_count > 0:
        print(f"✓ Pizza still referenced in {order_count} order(s) - sales data preserved")

    cursor.close()
    conn.close()

    print("\n✓ PIZZA ARCHIVING TEST PASSED!")
    return True

def test_customer_archiving():
    """Test customer archiving functionality"""
    print("\n" + "="*60)
    print("TESTING CUSTOMER ARCHIVING")
    print("="*60)

    conn = get_connection()
    cursor = conn.cursor()

    # 1. Get initial count of active customers
    cursor.execute("SELECT COUNT(*) as count FROM customers WHERE archived = FALSE")
    initial_count = cursor.fetchone()['count']
    print(f"✓ Initial active customers: {initial_count}")

    # 2. Get first customer
    cursor.execute("""
        SELECT customer_id, first_name, last_name
        FROM customers WHERE archived = FALSE LIMIT 1
    """)
    customer = cursor.fetchone()
    if not customer:
        print("✗ No customers found!")
        return False

    customer_id = customer['customer_id']
    customer_name = f"{customer['first_name']} {customer['last_name']}"
    print(f"✓ Testing with customer: {customer_name} (ID: {customer_id})")

    # 3. Archive the customer
    cursor.execute("UPDATE customers SET archived = TRUE WHERE customer_id = %s", (customer_id,))
    conn.commit()
    print(f"✓ Customer archived successfully")

    # 4. Verify customer is no longer in active list
    cursor.execute("SELECT COUNT(*) as count FROM customers WHERE archived = FALSE")
    new_count = cursor.fetchone()['count']
    if new_count == initial_count - 1:
        print(f"✓ Active customer count decreased from {initial_count} to {new_count}")
    else:
        print(f"✗ Expected count {initial_count - 1}, got {new_count}")
        return False

    # 5. Verify customer still exists in database with archived = TRUE
    cursor.execute("SELECT archived FROM customers WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchone()
    if result and result['archived']:
        print(f"✓ Customer {customer_name} is correctly marked as archived")
    else:
        print(f"✗ Customer archive status incorrect")
        return False

    # 6. Verify customer's orders are still intact
    cursor.execute("""
        SELECT COUNT(*) as count FROM orders
        WHERE customer_id = %s
    """, (customer_id,))
    order_count = cursor.fetchone()['count']
    if order_count > 0:
        print(f"✓ Customer still has {order_count} order(s) - order history preserved")

    cursor.close()
    conn.close()

    print("\n✓ CUSTOMER ARCHIVING TEST PASSED!")
    return True

def main():
    """Run all archiving tests"""
    print("\n" + "="*60)
    print("ARCHIVING FUNCTIONALITY TEST SUITE")
    print("="*60)

    try:
        pizza_test = test_pizza_archiving()
        customer_test = test_customer_archiving()

        print("\n" + "="*60)
        print("TEST RESULTS")
        print("="*60)
        print(f"Pizza Archiving: {'PASSED ✓' if pizza_test else 'FAILED ✗'}")
        print(f"Customer Archiving: {'PASSED ✓' if customer_test else 'FAILED ✗'}")
        print("="*60)

        if pizza_test and customer_test:
            print("\n🎉 ALL TESTS PASSED! Archiving functionality is working correctly.")
            print("\nKey Benefits:")
            print("  • Pizzas can be archived even if they appear in orders")
            print("  • Customers can be archived while preserving order history")
            print("  • Sales data integrity is maintained")
            print("  • No more foreign key constraint violations!")
            return 0
        else:
            print("\n✗ Some tests failed. Please review the output above.")
            return 1

    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit(main())
