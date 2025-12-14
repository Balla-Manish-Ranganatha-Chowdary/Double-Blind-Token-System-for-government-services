@echo off
echo ========================================
echo Checking PostgreSQL Database
echo ========================================
echo.

REM Check if PostgreSQL is installed
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PostgreSQL not found in PATH
    pause
    exit /b 1
)

echo Listing all databases...
echo.
psql -U postgres -c "\l"

echo.
echo ========================================
echo Checking if gov_services_db exists...
echo ========================================
echo.

psql -U postgres -c "SELECT datname FROM pg_database WHERE datname='gov_services_db';"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Database check complete!
) else (
    echo.
    echo Could not verify database
)

echo.
pause
