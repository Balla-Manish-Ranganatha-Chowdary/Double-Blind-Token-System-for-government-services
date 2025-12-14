# Scaling Guide - Government Portal

Quick reference for scaling the Government Portal system.

## Horizontal Scaling (Recommended)

### Docker Compose

**Scale backend**:
```bash
docker-compose up -d --scale backend=5
```

**Scale frontend**:
```bash
docker-compose up -d --scale frontend=3
```

**Scale workers**:
```bash
docker-compose up -d --scale celery-worker=4
```

**Scale all at once**:
```bash
docker-compose up -d --scale backend=5 --scale frontend=3 --scale celery-worker=4
```

### Kubernetes

**Manual scaling**:
```bash
# Backend
kubectl scale deployment backend --replicas=10 -n gov-portal

# Frontend
kubectl scale deployment frontend --replicas=5 -n gov-portal

# Workers
kubectl scale deployment celery-worker --replicas=6 -n gov-portal
```

**Automatic scaling** (already configured in `k8s/hpa.yaml`):
- Backend: 3-10 replicas (scales at 70% CPU)
- Frontend: 2-6 replicas (scales at 70% CPU)
- Workers: 2-8 replicas (scales at 75% CPU)

**Check autoscaling status**:
```bash
kubectl get hpa -n gov-portal
kubectl describe hpa backend-hpa -n gov-portal
```

**Watch autoscaling in action**:
```bash
kubectl get hpa -n gov-portal -w
```

## Vertical Scaling

### Increase Resources

**Docker Compose** - Edit `docker-compose.yml`:
```yaml
backend:
  deploy:
    resources:
      limits:
        cpus: '2'      # Increase from 1
        memory: 2G     # Increase from 1G
```

**Kubernetes** - Edit deployment files:
```yaml
resources:
  requests:
    memory: "1Gi"      # Increase from 512Mi
    cpu: "1000m"       # Increase from 500m
  limits:
    memory: "2Gi"      # Increase from 1Gi
    cpu: "2000m"       # Increase from 1000m
```

Apply changes:
```bash
kubectl apply -f k8s/backend-deployment.yaml
```

## Database Scaling

### Read Replicas

Already configured in `docker-compose.yml`. To use:

1. **Update Django settings**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'postgres-primary',
        ...
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'postgres-replica',
        ...
    }
}
```

2. **Use in views**:
```python
# Read from replica
Application.objects.using('replica').all()

# Write to primary (default)
Application.objects.create(...)
```

### Connection Pooling

Already configured in `backend/config/settings.py`:
```python
DATABASES['default']['CONN_MAX_AGE'] = 600
```

## Cache Scaling

### Redis Cluster

For high traffic, upgrade to Redis Cluster:

1. **Update docker-compose.yml**:
```yaml
redis-cluster:
  image: redis:7-alpine
  command: redis-cli --cluster create ...
```

2. **Update Django settings**:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            'redis://redis-1:6379/1',
            'redis://redis-2:6379/1',
            'redis://redis-3:6379/1',
        ],
    }
}
```

## When to Scale

### Metrics to Watch

**Scale UP when**:
- CPU usage > 70% for 5+ minutes
- Memory usage > 80% for 5+ minutes
- Response time > 2 seconds
- Request queue growing
- Error rate increasing

**Scale DOWN when**:
- CPU usage < 30% for 15+ minutes
- Memory usage < 40% for 15+ minutes
- Low traffic periods (nights/weekends)

### Check Current Metrics

**Docker**:
```bash
docker stats
```

**Kubernetes**:
```bash
kubectl top pods -n gov-portal
kubectl top nodes
```

**Prometheus**:
- CPU: `rate(process_cpu_seconds_total[5m])`
- Memory: `process_resident_memory_bytes`
- Requests: `rate(http_requests_total[5m])`

## Load Testing

### Before Scaling
```bash
# Current performance
k6 run --vus 100 --duration 2m loadtest.js
```

### After Scaling
```bash
# Test with higher load
k6 run --vus 500 --duration 5m loadtest.js
```

### Watch Autoscaling
```bash
# Terminal 1: Run load test
k6 run --vus 1000 --duration 10m loadtest.js

# Terminal 2: Watch scaling
kubectl get hpa -n gov-portal -w
```

## Cost Optimization

### Right-Sizing

1. **Monitor actual usage** for 1 week
2. **Adjust resource limits** to match usage + 20% buffer
3. **Set appropriate HPA thresholds**

### Spot Instances (Cloud)

Use spot instances for:
- Celery workers (can be interrupted)
- Development environments
- Testing environments

Don't use for:
- Database (needs stability)
- Backend API (needs reliability)

### Scheduled Scaling

Scale down during low-traffic periods:

**Kubernetes CronJob**:
```yaml
# Scale down at night (11 PM)
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-down-night
spec:
  schedule: "0 23 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: kubectl
            image: bitnami/kubectl
            command:
            - kubectl
            - scale
            - deployment
            - backend
            - --replicas=2
            - -n
            - gov-portal

# Scale up in morning (6 AM)
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-up-morning
spec:
  schedule: "0 6 * * *"
  ...
```

## Troubleshooting Scaling Issues

### Pods Not Scaling

**Check HPA**:
```bash
kubectl describe hpa backend-hpa -n gov-portal
```

**Common issues**:
- Metrics server not installed
- Resource requests not set
- Insufficient cluster resources

**Fix**:
```bash
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### High CPU Despite Scaling

**Possible causes**:
- Inefficient code/queries
- Memory leaks
- Too many database connections

**Solutions**:
- Optimize database queries
- Enable caching
- Increase connection pool
- Profile application code

### Database Bottleneck

**Symptoms**:
- Slow queries
- Connection timeouts
- High database CPU

**Solutions**:
- Add database indexes
- Enable query caching
- Use read replicas
- Upgrade database instance
- Implement connection pooling

## Quick Reference

| Action | Docker Compose | Kubernetes |
|--------|---------------|------------|
| Scale backend to 5 | `docker-compose up -d --scale backend=5` | `kubectl scale deployment backend --replicas=5 -n gov-portal` |
| Check status | `docker-compose ps` | `kubectl get pods -n gov-portal` |
| View metrics | `docker stats` | `kubectl top pods -n gov-portal` |
| View logs | `docker-compose logs -f backend` | `kubectl logs -f <pod> -n gov-portal` |
| Restart | `docker-compose restart backend` | `kubectl rollout restart deployment backend -n gov-portal` |

---

**Remember**: Always test scaling in staging before production!
