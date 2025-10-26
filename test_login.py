"""
Quick test to verify login is working
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

# Import Flask app
from app import app
from app.db_service import get_employee_by_email

def test_login_credentials():
    """Test that the default login credentials work"""
    print("\n" + "="*60)
    print("TESTING LOGIN CREDENTIALS")
    print("="*60)

    # Test credentials
    email = "john.manager@pizzashop.com"
    password = "password123"

    print(f"\nAttempting to fetch employee: {email}")

    try:
        # Use Flask application context
        with app.app_context():
            employee = get_employee_by_email(email)

            if employee:
                print(f"✓ Employee found:")
                print(f"  - ID: {employee.employee_id}")
                print(f"  - Name: {employee.first_name} {employee.last_name}")
                print(f"  - Email: {employee.email}")
                print(f"  - Role: {employee.role}")
                print(f"  - Active: {employee.active}")

                # Test password
                if employee.check_password(password):
                    print(f"\n✓ Password verification PASSED")
                    print(f"\n✅ LOGIN SHOULD WORK!")
                    print(f"\nLogin credentials:")
                    print(f"  Email: {email}")
                    print(f"  Password: {password}")
                    return True
                else:
                    print(f"\n✗ Password verification FAILED")
                    print(f"\n⚠️  The password '{password}' does not match!")
                    return False
            else:
                print(f"✗ Employee not found in database")
                print(f"\n⚠️  Employee with email '{email}' does not exist!")
                print(f"\nPlease run: python app/init_db.py")
                return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"\n⚠️  Database connection failed!")
        print(f"\nMake sure:")
        print(f"  1. MySQL is running")
        print(f"  2. Database is created")
        print(f"  3. .env file is configured correctly")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("LOGIN TROUBLESHOOTING TOOL")
    print("="*60)

    success = test_login_credentials()

    print("\n" + "="*60)
    if success:
        print("✅ Everything looks good! You should be able to login.")
        print("\nAccess the application at:")
        print("  http://127.0.0.1:5000/auth/login")
    else:
        print("⚠️  There's an issue preventing login.")
        print("Please review the errors above.")
    print("="*60)
