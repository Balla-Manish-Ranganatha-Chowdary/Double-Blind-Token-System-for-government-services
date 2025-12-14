@echo off
echo ========================================
echo Testing Autoscaling - Government Portal
echo ========================================
echo.

echo Step 1: Starting services with Docker Compose...
docker-compose up -d
echo.

echo Step 2: Waiting for services to be ready (30 seconds)...
timeout /t 30
echo.

echo Step 3: Checking service health...
curl http://localhost/api/health/
echo.
echo.

echo Step 4: Current service status:
docker-compose ps
echo.

echo Step 5: Scaling backend to 5 replicas...
docker-compose up -d --scale backend=3
echo.

echo Step 6: Scaling frontend to 3 replicas...
docker-compose up -d --scale frontend=2
echo.

echo Step 7: Scaling workers to 4 replicas...
docker-compose up -d --scale celery-worker=2
echo.

echo Step 8: Current resource usage:
docker stats --no-stream
echo.

echo ========================================
echo Autoscaling Test Complete!
echo ========================================
echo.
echo Access points:
echo - Application: http://localhost
echo - API Health: http://localhost/api/health/
echo - Prometheus: http://localhost:9090
echo - Grafana: http://localhost:3001 (admin/admin)
echo.
echo To run load test (requires k6):
echo   k6 run loadtest.js
echo.
echo To watch resource usage:
echo   docker stats
echo.
echo To stop all services:
echo   docker-compose down
echo.
pause
