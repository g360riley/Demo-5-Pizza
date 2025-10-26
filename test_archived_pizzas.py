"""
Test script for archived pizzas functionality
Tests archive, restore, and permanent delete operations
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from app.app_factory import create_app
from app.db_service import (
    get_all_pizzas,
    get_archived_pizzas,
    create_pizza,
    delete_pizza,
    restore_pizza,
    permanently_delete_pizza,
    get_pizza_by_id
)

def print_separator():
    print("\n" + "="*60 + "\n")

def test_archive_restore():
    """Test archiving and restoring pizzas"""
    app = create_app()

    with app.app_context():
        print("🧪 Testing Archived Pizzas Functionality")
        print_separator()

        # Test 1: Create a test pizza
        print("Test 1: Creating a test pizza...")
        pizza_id = create_pizza(
            "Test Archive Pizza",
            "Pizza for testing archive functionality",
            "Medium",
            12.99,
            "Classic",
            True
        )
        print(f"✅ Created pizza with ID: {pizza_id}")

        # Test 2: Verify it appears in active pizzas
        print("\nTest 2: Verifying pizza appears in active list...")
        active_pizzas = get_all_pizzas()
        pizza_names = [p.name for p in active_pizzas]
        assert "Test Archive Pizza" in pizza_names, "Pizza should be in active list"
        print(f"✅ Pizza found in active list ({len(active_pizzas)} total active pizzas)")

        # Test 3: Archive the pizza
        print("\nTest 3: Archiving the pizza...")
        success = delete_pizza(pizza_id)
        assert success, "Archive operation should succeed"
        print("✅ Pizza archived successfully")

        # Test 4: Verify it's removed from active list
        print("\nTest 4: Verifying pizza removed from active list...")
        active_pizzas = get_all_pizzas()
        pizza_names = [p.name for p in active_pizzas]
        assert "Test Archive Pizza" not in pizza_names, "Pizza should not be in active list"
        print(f"✅ Pizza removed from active list ({len(active_pizzas)} active pizzas remaining)")

        # Test 5: Verify it appears in archived list
        print("\nTest 5: Verifying pizza appears in archived list...")
        archived_pizzas = get_archived_pizzas()
        archived_names = [p.name for p in archived_pizzas]
        assert "Test Archive Pizza" in archived_names, "Pizza should be in archived list"
        print(f"✅ Pizza found in archived list ({len(archived_pizzas)} total archived pizzas)")

        # Test 6: Restore the pizza
        print("\nTest 6: Restoring the pizza...")
        success = restore_pizza(pizza_id)
        assert success, "Restore operation should succeed"
        print("✅ Pizza restored successfully")

        # Test 7: Verify it's back in active list
        print("\nTest 7: Verifying pizza is back in active list...")
        active_pizzas = get_all_pizzas()
        pizza_names = [p.name for p in active_pizzas]
        assert "Test Archive Pizza" in pizza_names, "Pizza should be back in active list"
        print(f"✅ Pizza restored to active list ({len(active_pizzas)} total active pizzas)")

        # Test 8: Verify it's removed from archived list
        print("\nTest 8: Verifying pizza removed from archived list...")
        archived_pizzas = get_archived_pizzas()
        archived_names = [p.name for p in archived_pizzas]
        assert "Test Archive Pizza" not in archived_names, "Pizza should not be in archived list"
        print(f"✅ Pizza removed from archived list ({len(archived_pizzas)} archived pizzas remaining)")

        # Test 9: Permanent delete (should succeed - no orders reference it)
        print("\nTest 9: Permanently deleting the pizza...")
        try:
            success = permanently_delete_pizza(pizza_id)
            assert success, "Permanent delete should succeed"
            print("✅ Pizza permanently deleted successfully")
        except Exception as e:
            print(f"❌ Permanent delete failed: {str(e)}")
            raise

        # Test 10: Verify pizza is completely gone
        print("\nTest 10: Verifying pizza is completely deleted...")
        pizza = get_pizza_by_id(pizza_id)
        assert pizza is None, "Pizza should not exist in database"
        print("✅ Pizza completely removed from database")

        print_separator()
        print("🎉 All tests passed!")
        print_separator()

def test_permanent_delete_with_orders():
    """Test that permanent delete fails when pizza is referenced in orders"""
    app = create_app()

    with app.app_context():
        print("🧪 Testing Permanent Delete with Foreign Key Constraint")
        print_separator()

        # Try to permanently delete a pizza that's in orders (should have pizza_id 1-3 from seed data)
        print("Test: Attempting to permanently delete pizza that's in orders...")
        pizza_id = 1  # Margherita from seed data

        pizza = get_pizza_by_id(pizza_id)
        if pizza:
            print(f"Found pizza: {pizza.name} (ID: {pizza_id})")

            try:
                permanently_delete_pizza(pizza_id)
                print("❌ FAIL: Should have raised an exception due to foreign key constraint")
            except Exception as e:
                if 'foreign key constraint' in str(e).lower() or 'cannot delete' in str(e).lower():
                    print(f"✅ PASS: Correctly prevented deletion due to foreign key constraint")
                    print(f"   Error message: {str(e)}")
                else:
                    print(f"❌ FAIL: Different error occurred: {str(e)}")
        else:
            print("⚠️  Warning: Pizza ID 1 not found, skipping this test")

        print_separator()

if __name__ == "__main__":
    try:
        test_archive_restore()
        test_permanent_delete_with_orders()
        print("\n✅ All archive functionality tests completed successfully!\n")
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
