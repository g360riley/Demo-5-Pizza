"""
Automated test script for session security implementation
Tests logout functionality and cache-control headers
"""
import requests
import sys
from urllib.parse import urljoin

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

def create_session():
    """Create a new requests session"""
    return requests.Session()

def test_protected_page_without_login():
    """Test that protected pages require login"""
    print("\n" + "="*60)
    print("TEST 1: Protected Page Without Login")
    print("="*60)

    session = create_session()
    response = session.get(urljoin(BASE_URL, "/dashboard"), allow_redirects=True)

    # Check if redirected to login
    if "/auth/login" in response.url:
        print("✓ Protected page redirects to login when not authenticated")
        return True
    else:
        print(f"✗ Expected redirect to /auth/login, got {response.url}")
        return False

def test_cache_headers_on_authenticated_page():
    """Test that authenticated pages have no-cache headers"""
    print("\n" + "="*60)
    print("TEST 2: Cache Headers on Authenticated Pages")
    print("="*60)

    session = create_session()

    # Login first
    login_data = {
        'email': 'john.manager@pizzashop.com',
        'password': 'password123'
    }
    login_response = session.post(urljoin(BASE_URL, "/auth/login"), data=login_data)

    if login_response.status_code != 200 and login_response.status_code != 302:
        print(f"✗ Login failed with status {login_response.status_code}")
        return False

    # Visit protected page
    response = session.get(urljoin(BASE_URL, "/dashboard"))

    # Check headers
    cache_control = response.headers.get('Cache-Control', '')
    pragma = response.headers.get('Pragma', '')
    expires = response.headers.get('Expires', '')

    print(f"Cache-Control: {cache_control}")
    print(f"Pragma: {pragma}")
    print(f"Expires: {expires}")

    checks = [
        ('no-cache' in cache_control, "Cache-Control contains 'no-cache'"),
        ('no-store' in cache_control, "Cache-Control contains 'no-store'"),
        ('must-revalidate' in cache_control, "Cache-Control contains 'must-revalidate'"),
        (pragma == 'no-cache', "Pragma is 'no-cache'"),
        (expires == '0', "Expires is '0'")
    ]

    all_passed = True
    for passed, description in checks:
        if passed:
            print(f"✓ {description}")
        else:
            print(f"✗ {description}")
            all_passed = False

    return all_passed

def test_logout_clears_session():
    """Test that logout properly clears session"""
    print("\n" + "="*60)
    print("TEST 3: Logout Clears Session")
    print("="*60)

    session = create_session()

    # Login
    login_data = {
        'email': 'john.manager@pizzashop.com',
        'password': 'password123'
    }
    session.post(urljoin(BASE_URL, "/auth/login"), data=login_data)
    print("✓ Logged in successfully")

    # Verify we can access protected page
    response = session.get(urljoin(BASE_URL, "/dashboard"))
    if response.status_code == 200 and "/auth/login" not in response.url:
        print("✓ Can access protected page while logged in")
    else:
        print("✗ Cannot access protected page while logged in")
        return False

    # Logout
    session.get(urljoin(BASE_URL, "/auth/logout"))
    print("✓ Logged out")

    # Try to access protected page again
    response = session.get(urljoin(BASE_URL, "/dashboard"), allow_redirects=True)

    if "/auth/login" in response.url:
        print("✓ Cannot access protected page after logout (redirected to login)")
        return True
    else:
        print(f"✗ Still able to access protected page after logout")
        print(f"   Response URL: {response.url}")
        return False

def test_logout_response_headers():
    """Test that logout response has cache-control headers"""
    print("\n" + "="*60)
    print("TEST 4: Logout Response Headers")
    print("="*60)

    session = create_session()

    # Login
    login_data = {
        'email': 'john.manager@pizzashop.com',
        'password': 'password123'
    }
    session.post(urljoin(BASE_URL, "/auth/login"), data=login_data)
    print("✓ Logged in successfully")

    # Logout and check headers (don't follow redirects)
    response = session.get(urljoin(BASE_URL, "/auth/logout"), allow_redirects=False)

    cache_control = response.headers.get('Cache-Control', '')
    pragma = response.headers.get('Pragma', '')

    print(f"Logout Response Cache-Control: {cache_control}")
    print(f"Logout Response Pragma: {pragma}")

    if 'no-cache' in cache_control and 'no-store' in cache_control:
        print("✓ Logout response has proper cache-control headers")
        return True
    else:
        print("✗ Logout response missing cache-control headers")
        return False

def test_multiple_protected_pages():
    """Test that multiple protected pages are secured"""
    print("\n" + "="*60)
    print("TEST 5: Multiple Protected Pages After Logout")
    print("="*60)

    session = create_session()

    # Login
    login_data = {
        'email': 'john.manager@pizzashop.com',
        'password': 'password123'
    }
    session.post(urljoin(BASE_URL, "/auth/login"), data=login_data)
    print("✓ Logged in successfully")

    # Logout
    session.get(urljoin(BASE_URL, "/auth/logout"))
    print("✓ Logged out")

    # Test multiple protected pages
    protected_pages = [
        "/dashboard",
        "/pizzas",
        "/customers",
        "/orders",
        "/employees",
        "/auth/profile"
    ]

    all_passed = True
    for page in protected_pages:
        response = session.get(urljoin(BASE_URL, page), allow_redirects=True)
        if "/auth/login" in response.url:
            print(f"✓ {page} redirects to login")
        else:
            print(f"✗ {page} does not redirect to login")
            all_passed = False

    return all_passed

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SESSION SECURITY TEST SUITE")
    print("="*60)
    print(f"Testing application at: {BASE_URL}")
    print("="*60)

    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print("✓ Server is running")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure the Flask app is running.")
        print(f"   Start the server with: python app.py")
        return 1
    except Exception as e:
        print(f"✗ Error connecting to server: {e}")
        return 1

    # Run tests
    tests = [
        ("Protected Page Without Login", test_protected_page_without_login),
        ("Cache Headers on Authenticated Pages", test_cache_headers_on_authenticated_page),
        ("Logout Clears Session", test_logout_clears_session),
        ("Logout Response Headers", test_logout_response_headers),
        ("Multiple Protected Pages After Logout", test_multiple_protected_pages)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")

    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)

    if passed == total:
        print("\n🎉 All tests passed! Session security is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
