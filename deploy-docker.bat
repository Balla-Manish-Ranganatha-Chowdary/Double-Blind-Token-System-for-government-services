@echo off
echo ========================================
echo Government Portal - Docker Deployment
echo ========================================
echo.

echo Step 1: Checking environment file...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please update .env with your configuration!
    pause
)

echo.
echo Step 2: Building Docker images...
docker-compose build

echo.
echo Step 3: Starting services...
docker-compose up -d

echo.
echo Step 4: Waiting for database to be ready...
timeout /t 10

echo.
echo Step 5: Running migrations...
docker-compose exec backend python manage.py migrate

echo.
echo Step 6: Creating superuser (optional)...
docker-compose exec backend python manage.py createsuperuser

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Services:
echo - Frontend: http://localhost
echo - Backend API: http://localhost/api
echo - Admin: http://localhost/admin
echo - Prometheus: http://localhost:9090
echo - Grafana: http://localhost:3000
echo.
echo Check status: docker-compose ps
echo View logs: docker-compose logs -f
echo Stop services: docker-compose down
echo.
pause
