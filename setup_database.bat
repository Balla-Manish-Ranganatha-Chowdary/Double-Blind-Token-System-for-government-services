@echo off
echo ========================================
echo PostgreSQL Database Setup
echo Government Services Portal
echo ========================================
echo.

REM Check if PostgreSQL is installed
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PostgreSQL not found in PATH
    echo.
    echo Please add PostgreSQL bin directory to PATH or run:
    echo "C:\Program Files\PostgreSQL\15\bin\psql" -U postgres -f setup_database.sql
    echo.
    pause
    exit /b 1
)

echo Creating database gov_services_db...
echo.

REM Run SQL script
psql -U postgres -c "CREATE DATABASE gov_services_db;"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Database created successfully
    echo ========================================
    echo.
    echo Database name: gov_services_db
    echo.
    echo Next steps:
    echo 1. Update backend/.env with your database credentials
    echo 2. Run: cd backend
    echo 3. Run: python manage.py migrate
    echo 4. Run: python setup_db.py
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Failed to create database
    echo ========================================
    echo.
    echo Possible reasons:
    echo - Database already exists (this is OK!)
    echo - Wrong password
    echo - PostgreSQL service not running
    echo.
    echo To check if database exists:
    echo psql -U postgres -l
    echo.
)

pause
