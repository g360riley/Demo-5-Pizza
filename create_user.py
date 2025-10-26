"""
Create a new employee account
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

from app import app
from app.db_connect import get_db
from werkzeug.security import generate_password_hash
from datetime import date

def create_employee(first_name, last_name, email, phone, role, password):
    """Create a new employee"""
    with app.app_context():
        db = get_db()
        if not db:
            print("✗ Could not connect to database")
            return False

        cursor = db.cursor()

        # Check if employee already exists
        cursor.execute("SELECT email FROM employees WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"✓ Employee with email {email} already exists")
            cursor.close()
            return True

        # Create new employee
        password_hash = generate_password_hash(password)
        hire_date = date.today()

        cursor.execute("""
            INSERT INTO employees (first_name, last_name, email, phone, role, password_hash, hire_date, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, role, password_hash, hire_date, True))

        db.commit()
        cursor.close()

        print(f"✓ Employee created successfully!")
        print(f"  Name: {first_name} {last_name}")
        print(f"  Email: {email}")
        print(f"  Role: {role}")
        return True

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CREATE EMPLOYEE ACCOUNT")
    print("="*60)

    # Create Gage Manager account
    success = create_employee(
        first_name="Gage",
        last_name="Manager",
        email="gage.manager@pizzashop.com",
        phone="555-0999",
        role="Manager",
        password="password123"
    )

    if success:
        print("\n" + "="*60)
        print("✅ Account ready!")
        print("\nYou can now login with:")
        print("  Email: gage.manager@pizzashop.com")
        print("  Password: password123")
        print("\nLogin at: http://127.0.0.1:5000/auth/login")
        print("="*60)
    else:
        print("\n✗ Failed to create account")
