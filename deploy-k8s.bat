@echo off
echo ========================================
echo Government Portal - Kubernetes Deployment
echo ========================================
echo.

echo Step 1: Creating namespace...
kubectl apply -f k8s/namespace.yaml

echo.
echo Step 2: Applying secrets and config...
echo WARNING: Update k8s/secrets.yaml with your values first!
pause
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml

echo.
echo Step 3: Deploying database and cache...
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/redis-deployment.yaml

echo.
echo Step 4: Waiting for database to be ready...
timeout /t 20

echo.
echo Step 5: Deploying application...
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/celery-deployment.yaml

echo.
echo Step 6: Enabling autoscaling...
kubectl apply -f k8s/hpa.yaml

echo.
echo Step 7: Setting up ingress...
kubectl apply -f k8s/ingress.yaml

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Check status:
kubectl get pods -n gov-portal
echo.
kubectl get hpa -n gov-portal
echo.
echo View logs: kubectl logs -f <pod-name> -n gov-portal
echo Scale manually: kubectl scale deployment backend --replicas=5 -n gov-portal
echo.
pause
