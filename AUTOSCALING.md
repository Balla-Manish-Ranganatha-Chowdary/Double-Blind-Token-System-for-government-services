# Government Portal - Autoscaling Guide

Complete guide for deploying and scaling the Government Services Portal using Docker Compose and Kubernetes.

## Architecture Overview

The system is designed for horizontal scaling with:
- **Backend**: Django with Gunicorn (3-10 replicas)
- **Frontend**: Next.js (2-6 replicas)
- **Workers**: Celery workers (2-8 replicas)
- **Database**: PostgreSQL with read replicas
- **Cache**: Redis for sessions and caching
- **Load Balancer**: Nginx
- **Monitoring**: Prometheus + Grafana

## Quick Start

### Docker Compose (Development/Testing)

1. **Build images**:
```bash
docker-compose build
```

2. **Start services**:
```bash
docker-compose up -d
```

3. **Check status**:
```bash
docker-compose ps
```

4. **View logs**:
```bash
docker-compose logs -f backend
```

5. **Scale services**:
```bash
docker-compose up -d --scale backend=5 --scale frontend=3
```

### Kubernetes (Production)

1. **Create namespace**:
```bash
kubectl apply -f k8s/namespace.yaml
```

2. **Create secrets** (update with your values first):
```bash
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml
```

3. **Deploy database and cache**:
```bash
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/redis-deployment.yaml
```

4. **Deploy application**:
```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/celery-deployment.yaml
```

5. **Enable autoscaling**:
```bash
kubectl apply -f k8s/hpa.yaml
```

6. **Setup ingress**:
```bash
kubectl apply -f k8s/ingress.yaml
```

7. **Verify deployment**:
```bash
kubectl get pods -n gov-portal
kubectl get hpa -n gov-portal
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and update:

```bash
# Generate encryption keys
python backend/generate_keys.py

# Update .env with generated keys
SECRET_KEY=your-secret-key
ENCRYPTION_KEY=generated-key-1
ENCRYPTION_KEY_SECONDARY=generated-key-2
DB_PASSWORD=secure-password
REDIS_PASSWORD=redis-password
```

### Scaling Configuration

**Docker Compose** - Edit `docker-compose.yml`:
```yaml
deploy:
  replicas: 5  # Change replica count
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

**Kubernetes** - Edit `k8s/hpa.yaml`:
```yaml
minReplicas: 3
maxReplicas: 10
metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        averageUtilization: 70  # Scale at 70% CPU
```

## Monitoring

### Access Monitoring Tools

**Prometheus**: http://localhost:9090
- View metrics and queries
- Check target health

**Grafana**: http://localhost:3000
- Default credentials: admin/admin
- Pre-configured dashboards for system metrics

### Key Metrics to Monitor

- **CPU Usage**: `rate(process_cpu_seconds_total[5m])`
- **Memory Usage**: `process_resident_memory_bytes`
- **Request Rate**: `rate(http_requests_total[5m])`
- **Response Time**: `http_request_duration_seconds`
- **Error Rate**: `rate(http_requests_total{status=~"5.."}[5m])`

### Alerts

Configured in `monitoring/alerts.yml`:
- High CPU usage (>80% for 5 minutes)
- High memory usage (>85% for 5 minutes)
- Service down (>2 minutes)
- High response time (>2 seconds)
- Database connection issues

## Load Testing

Test autoscaling with Apache Bench or k6:

```bash
# Apache Bench
ab -n 10000 -c 100 http://localhost/api/applications/

# k6
k6 run --vus 100 --duration 5m loadtest.js
```

Watch pods scale:
```bash
kubectl get hpa -n gov-portal -w
```

## Database Scaling

### Read Replicas

PostgreSQL replica is configured in `docker-compose.yml` for read operations.

Update Django settings to use read replica:
```python
DATABASES = {
    'default': {...},
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'postgres-replica',
        ...
    }
}
```

## Production Deployment

### Build Production Images

```bash
# Backend
docker build -t gov-portal-backend:latest ./backend

# Frontend
docker build -t gov-portal-frontend:latest ./frontend

# Tag for registry
docker tag gov-portal-backend:latest your-registry/gov-portal-backend:latest
docker tag gov-portal-frontend:latest your-registry/gov-portal-frontend:latest

# Push to registry
docker push your-registry/gov-portal-backend:latest
docker push your-registry/gov-portal-frontend:latest
```

### Update Kubernetes Deployments

Edit image references in deployment files:
```yaml
image: your-registry/gov-portal-backend:latest
```

### SSL/TLS Configuration

Add SSL certificates to ingress:
```yaml
spec:
  tls:
  - hosts:
    - gov-portal.yourdomain.com
    secretName: tls-secret
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -n gov-portal
kubectl describe pod <pod-name> -n gov-portal
kubectl logs <pod-name> -n gov-portal
```

### Check HPA Status
```bash
kubectl get hpa -n gov-portal
kubectl describe hpa backend-hpa -n gov-portal
```

### Database Connection Issues
```bash
# Test database connection
kubectl exec -it <backend-pod> -n gov-portal -- python manage.py dbshell
```

### Redis Connection Issues
```bash
# Test Redis connection
kubectl exec -it <backend-pod> -n gov-portal -- redis-cli -h redis-service -a $REDIS_PASSWORD ping
```

## Performance Optimization

### Backend Optimization

1. **Enable caching**:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

2. **Database connection pooling**:
```python
DATABASES['default']['CONN_MAX_AGE'] = 600
```

3. **Gunicorn workers**: Adjust based on CPU cores
```bash
workers = (2 * cpu_cores) + 1
```

### Frontend Optimization

1. **Enable Next.js caching**
2. **Use CDN for static assets**
3. **Enable image optimization**

### Nginx Optimization

Already configured in `nginx/nginx.conf`:
- Gzip compression
- Connection pooling
- Static file caching
- Load balancing with least_conn

## Cost Optimization

### Resource Limits

Set appropriate limits in deployments:
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

### Autoscaling Thresholds

Adjust HPA thresholds based on usage patterns:
- Lower thresholds = more responsive but higher cost
- Higher thresholds = lower cost but slower response

### Spot Instances

Use spot instances for non-critical workloads:
- Celery workers
- Development environments
- Testing environments

## Backup and Recovery

### Database Backups

```bash
# Manual backup
kubectl exec -it postgres-0 -n gov-portal -- pg_dump -U postgres government_services > backup.sql

# Restore
kubectl exec -i postgres-0 -n gov-portal -- psql -U postgres government_services < backup.sql
```

### Automated Backups

Configure CronJob for automated backups (create `k8s/backup-cronjob.yaml`).

## Security

1. **Update secrets** in `k8s/secrets.yaml` with strong passwords
2. **Enable network policies** to restrict pod communication
3. **Use RBAC** for Kubernetes access control
4. **Enable SSL/TLS** for all external traffic
5. **Regular security updates** for base images

## Support

For issues or questions:
1. Check logs: `kubectl logs <pod-name> -n gov-portal`
2. Check events: `kubectl get events -n gov-portal`
3. Review monitoring dashboards in Grafana
4. Check Prometheus alerts
