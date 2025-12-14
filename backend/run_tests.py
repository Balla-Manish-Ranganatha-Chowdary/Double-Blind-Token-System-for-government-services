"""
Test runner script to execute all unit tests
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    print("=" * 70)
    print("Running Unit Tests for Government Portal")
    print("=" * 70)
    print()
    
    # Run all tests
    failures = test_runner.run_tests([
        "apps.encryption.tests",
        "apps.applications.tests",
        "apps.officers.tests",
        "apps.ai_services.tests",
    ])
    
    print()
    print("=" * 70)
    if failures:
        print(f"FAILED: {failures} test(s) failed")
        sys.exit(1)
    else:
        print("SUCCESS: All tests passed!")
    print("=" * 70)
