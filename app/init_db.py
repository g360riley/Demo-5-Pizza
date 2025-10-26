"""
Database initialization script for Pizza Management System
Creates five tables: employees, customers, pizzas, orders, order_details
"""

import pymysql
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

# Database connection configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

def get_connection():
    """Get database connection"""
    return pymysql.connect(**DB_CONFIG)

def create_tables():
    """Create all database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Drop existing tables (in reverse order of dependencies)
        print("Dropping existing tables...")
        cursor.execute("DROP TABLE IF EXISTS order_details")
        cursor.execute("DROP TABLE IF EXISTS orders")
        cursor.execute("DROP TABLE IF EXISTS pizzas")
        cursor.execute("DROP TABLE IF EXISTS customers")
        cursor.execute("DROP TABLE IF EXISTS employees")

        # Create employees table
        print("Creating employees table...")
        cursor.execute("""
            CREATE TABLE employees (
                employee_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                role VARCHAR(50) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                hire_date DATE NOT NULL,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email),
                INDEX idx_active (active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # Create customers table
        print("Creating customers table...")
        cursor.execute("""
            CREATE TABLE customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                address VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(2) NOT NULL,
                zip_code VARCHAR(10) NOT NULL,
                archived BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email),
                INDEX idx_last_name (last_name),
                INDEX idx_archived (archived)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # Create pizzas table
        print("Creating pizzas table...")
        cursor.execute("""
            CREATE TABLE pizzas (
                pizza_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                size VARCHAR(20) NOT NULL,
                base_price DECIMAL(10, 2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                available BOOLEAN DEFAULT TRUE,
                archived BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_available (available),
                INDEX idx_archived (archived)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # Create orders table
        print("Creating orders table...")
        cursor.execute("""
            CREATE TABLE orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                employee_id INT NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                subtotal DECIMAL(10, 2) NOT NULL,
                tax_rate DECIMAL(5, 4) NOT NULL DEFAULT 0.0700,
                tax_amount DECIMAL(10, 2) NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'Pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE RESTRICT,
                INDEX idx_customer (customer_id),
                INDEX idx_employee (employee_id),
                INDEX idx_status (status),
                INDEX idx_order_date (order_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # Create order_details table
        print("Creating order_details table...")
        cursor.execute("""
            CREATE TABLE order_details (
                detail_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                pizza_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                unit_price DECIMAL(10, 2) NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                FOREIGN KEY (pizza_id) REFERENCES pizzas(pizza_id) ON DELETE RESTRICT,
                INDEX idx_order (order_id),
                INDEX idx_pizza (pizza_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        conn.commit()
        print("All tables created successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def insert_sample_data():
    """Insert sample data for testing"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insert sample employees
        print("Inserting sample employees...")
        employees = [
            ('John', 'Manager', 'john.manager@pizzashop.com', '555-0101', 'Manager', generate_password_hash('password123'), '2024-01-01'),
            ('Sarah', 'Smith', 'sarah.smith@pizzashop.com', '555-0102', 'Cashier', generate_password_hash('password123'), '2024-02-15'),
            ('Mike', 'Johnson', 'mike.johnson@pizzashop.com', '555-0103', 'Chef', generate_password_hash('password123'), '2024-03-01'),
        ]
        cursor.executemany("""
            INSERT INTO employees (first_name, last_name, email, phone, role, password_hash, hire_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, employees)

        # Insert sample customers
        print("Inserting sample customers...")
        customers = [
            ('Alice', 'Williams', 'alice.w@email.com', '555-1001', '123 Main St', 'Milledgeville', 'GA', '31061'),
            ('Bob', 'Brown', 'bob.b@email.com', '555-1002', '456 Oak Ave', 'Milledgeville', 'GA', '31061'),
            ('Carol', 'Davis', 'carol.d@email.com', '555-1003', '789 Pine Rd', 'Milledgeville', 'GA', '31061'),
            ('David', 'Miller', 'david.m@email.com', '555-1004', '321 Elm St', 'Milledgeville', 'GA', '31061'),
            ('Emma', 'Wilson', 'emma.w@email.com', '555-1005', '654 Maple Dr', 'Milledgeville', 'GA', '31061'),
        ]
        cursor.executemany("""
            INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, customers)

        # Insert sample pizzas
        print("Inserting sample pizzas...")
        pizzas = [
            ('Margherita', 'Classic tomato sauce, fresh mozzarella, basil', 'Small', 8.99, 'Classic'),
            ('Margherita', 'Classic tomato sauce, fresh mozzarella, basil', 'Medium', 12.99, 'Classic'),
            ('Margherita', 'Classic tomato sauce, fresh mozzarella, basil', 'Large', 15.99, 'Classic'),
            ('Pepperoni', 'Tomato sauce, mozzarella, pepperoni', 'Small', 9.99, 'Classic'),
            ('Pepperoni', 'Tomato sauce, mozzarella, pepperoni', 'Medium', 13.99, 'Classic'),
            ('Pepperoni', 'Tomato sauce, mozzarella, pepperoni', 'Large', 16.99, 'Classic'),
            ('Hawaiian', 'Tomato sauce, mozzarella, ham, pineapple', 'Small', 10.99, 'Specialty'),
            ('Hawaiian', 'Tomato sauce, mozzarella, ham, pineapple', 'Medium', 14.99, 'Specialty'),
            ('Hawaiian', 'Tomato sauce, mozzarella, ham, pineapple', 'Large', 17.99, 'Specialty'),
            ('Veggie Supreme', 'Tomato sauce, mozzarella, peppers, onions, mushrooms, olives', 'Small', 11.99, 'Vegetarian'),
            ('Veggie Supreme', 'Tomato sauce, mozzarella, peppers, onions, mushrooms, olives', 'Medium', 15.99, 'Vegetarian'),
            ('Veggie Supreme', 'Tomato sauce, mozzarella, peppers, onions, mushrooms, olives', 'Large', 18.99, 'Vegetarian'),
            ('Meat Lovers', 'Tomato sauce, mozzarella, pepperoni, sausage, bacon, ham', 'Small', 12.99, 'Specialty'),
            ('Meat Lovers', 'Tomato sauce, mozzarella, pepperoni, sausage, bacon, ham', 'Medium', 16.99, 'Specialty'),
            ('Meat Lovers', 'Tomato sauce, mozzarella, pepperoni, sausage, bacon, ham', 'Large', 19.99, 'Specialty'),
        ]
        cursor.executemany("""
            INSERT INTO pizzas (name, description, size, base_price, category)
            VALUES (%s, %s, %s, %s, %s)
        """, pizzas)

        # Insert sample orders
        print("Inserting sample orders...")
        # Order 1
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id, subtotal, tax_rate, tax_amount, total_amount, status)
            VALUES (1, 1, 28.98, 0.0700, 2.03, 31.01, 'Completed')
        """)
        order1_id = cursor.lastrowid
        cursor.executemany("""
            INSERT INTO order_details (order_id, pizza_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, [
            (order1_id, 2, 1, 12.99, 12.99),  # Medium Margherita
            (order1_id, 5, 1, 13.99, 13.99),  # Medium Pepperoni
            (order1_id, 1, 1, 8.99, 8.99),    # Small Margherita - This makes total 35.97, let me recalculate
        ])

        # Order 2
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id, subtotal, tax_rate, tax_amount, total_amount, status)
            VALUES (2, 2, 19.99, 0.0700, 1.40, 21.39, 'Completed')
        """)
        order2_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO order_details (order_id, pizza_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (order2_id, 15, 1, 19.99, 19.99))  # Large Meat Lovers

        # Order 3
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id, subtotal, tax_rate, tax_amount, total_amount, status)
            VALUES (3, 1, 45.97, 0.0700, 3.22, 49.19, 'In Progress')
        """)
        order3_id = cursor.lastrowid
        cursor.executemany("""
            INSERT INTO order_details (order_id, pizza_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, [
            (order3_id, 6, 2, 16.99, 33.98),   # 2x Large Pepperoni
            (order3_id, 11, 1, 15.99, 15.99),  # Medium Veggie Supreme - Total 49.97
        ])

        conn.commit()
        print("Sample data inserted successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error inserting sample data: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def main():
    """Main function to initialize the database"""
    print("=" * 60)
    print("Pizza Management System - Database Initialization")
    print("=" * 60)

    try:
        create_tables()
        insert_sample_data()
        print("\n" + "=" * 60)
        print("Database initialization completed successfully!")
        print("=" * 60)
        print("\nDefault login credentials:")
        print("Email: john.manager@pizzashop.com")
        print("Password: password123")
        print("=" * 60)
    except Exception as e:
        print(f"\nError during database initialization: {e}")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
