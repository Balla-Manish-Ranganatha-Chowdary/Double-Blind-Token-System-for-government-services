@echo off
echo ========================================
echo Government Portal - Unit Testing
echo ========================================
echo.

echo Step 1: Setting up test environment...
cd backend
echo.

echo Step 2: Running encryption tests...
python manage.py test apps.encryption.tests --verbosity=2
echo.

echo Step 3: Running application tests...
python manage.py test apps.applications.tests --verbosity=2
echo.

echo Step 4: Running officer tests...
python manage.py test apps.officers.tests --verbosity=2
echo.

echo Step 5: Running AI services tests...
python manage.py test apps.ai_services.tests --verbosity=2
echo.

echo Step 6: Running all tests together...
python manage.py test --verbosity=2
echo.

echo ========================================
echo Testing Complete!
echo ========================================
echo.
echo Check the output above for any failures.
echo.
pause
