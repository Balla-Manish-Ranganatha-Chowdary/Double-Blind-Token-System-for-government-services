# Production Deployment Checklist

Complete checklist for deploying the Government Portal to production.

## Pre-Deployment

### Security
- [ ] Generate new encryption keys (`python backend/generate_keys.py`)
- [ ] Update `SECRET_KEY` in `.env` with strong random value
- [ ] Change all default passwords (database, Redis, Grafana)
- [ ] Update `k8s/secrets.yaml` with production values
- [ ] Enable SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up VPN for admin access

### Configuration
- [ ] Set `DEBUG=False` in backend settings
- [ ] Update `ALLOWED_HOSTS` with production domain
- [ ] Configure CORS origins for production frontend
- [ ] Set up production database (PostgreSQL)
- [ ] Configure Redis for production
- [ ] Update `NEXT_PUBLIC_API_URL` in frontend

### Infrastructure
- [ ] Provision servers/cloud instances
- [ ] Set up Kubernetes cluster (if using K8s)
- [ ] Configure load balancer
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure backup system
- [ ] Set up logging aggregation

## Docker Deployment

### Build Images
```bash
# Backend
cd backend
docker build -t gov-portal-backend:v1.0 .

# Frontend
cd frontend
docker build -t gov-portal-frontend:v1.0 .
```

### Push to Registry
```bash
# Tag images
docker tag gov-portal-backend:v1.0 your-registry/gov-portal-backend:v1.0
docker tag gov-portal-frontend:v1.0 your-registry/gov-portal-frontend:v1.0

# Push
docker push your-registry/gov-portal-backend:v1.0
docker push your-registry/gov-portal-frontend:v1.0
```

### Deploy with Docker Compose
```bash
# Update .env with production values
cp .env.example .env
nano .env

# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

## Kubernetes Deployment

### Prepare Cluster
```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Update secrets
nano k8s/secrets.yaml
kubectl apply -f k8s/secrets.yaml

# Apply config
kubectl apply -f k8s/configmap.yaml
```

### Deploy Infrastructure
```bash
# Database
kubectl apply -f k8s/postgres-deployment.yaml

# Cache
kubectl apply -f k8s/redis-deployment.yaml

# Wait for ready
kubectl wait --for=condition=ready pod -l app=postgres -n gov-portal --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n gov-portal --timeout=300s
```

### Deploy Application
```bash
# Backend
kubectl apply -f k8s/backend-deployment.yaml

# Frontend
kubectl apply -f k8s/frontend-deployment.yaml

# Workers
kubectl apply -f k8s/celery-deployment.yaml

# Wait for ready
kubectl wait --for=condition=ready pod -l app=backend -n gov-portal --timeout=300s
```

### Enable Autoscaling
```bash
# Apply HPA
kubectl apply -f k8s/hpa.yaml

# Verify
kubectl get hpa -n gov-portal
```

### Configure Ingress
```bash
# Update ingress with your domain
nano k8s/ingress.yaml

# Apply
kubectl apply -f k8s/ingress.yaml

# Verify
kubectl get ingress -n gov-portal
```

## Post-Deployment

### Database Setup
```bash
# Run migrations
kubectl exec -it <backend-pod> -n gov-portal -- python manage.py migrate

# Create superuser
kubectl exec -it <backend-pod> -n gov-portal -- python manage.py createsuperuser

# Load initial data
kubectl exec -it <backend-pod> -n gov-portal -- python setup_db.py
```

### Verification
- [ ] Test homepage loads
- [ ] Test API health endpoint: `/api/health/`
- [ ] Test citizen application submission
- [ ] Test officer login and dashboard
- [ ] Test admin login and dashboard
- [ ] Verify SSL certificate
- [ ] Check monitoring dashboards

### Monitoring Setup
```bash
# Access Prometheus
kubectl port-forward svc/prometheus -n gov-portal 9090:9090

# Access Grafana
kubectl port-forward svc/grafana -n gov-portal 3000:3000
```

- [ ] Configure Grafana dashboards
- [ ] Set up alert notifications (email/Slack)
- [ ] Test alert rules
- [ ] Configure log aggregation

### Backup Configuration
```bash
# Database backup script
kubectl create cronjob db-backup \
  --image=postgres:15-alpine \
  --schedule="0 2 * * *" \
  --restart=OnFailure \
  -- /bin/sh -c "pg_dump -h postgres-service -U postgres government_services > /backup/db-$(date +%Y%m%d).sql"
```

- [ ] Set up automated database backups
- [ ] Test backup restoration
- [ ] Configure backup retention policy
- [ ] Set up media files backup

## Load Testing

### Install k6
```bash
# Windows (Chocolatey)
choco install k6

# Linux
sudo apt-get install k6

# Mac
brew install k6
```

### Run Load Tests
```bash
# Basic test
k6 run loadtest.js

# Heavy load
k6 run --vus 500 --duration 10m loadtest.js

# Watch autoscaling
kubectl get hpa -n gov-portal -w
```

- [ ] Run load tests
- [ ] Verify autoscaling works
- [ ] Check response times under load
- [ ] Monitor resource usage
- [ ] Verify error rates are acceptable

## Performance Optimization

### Backend
- [ ] Enable database connection pooling
- [ ] Configure Redis caching
- [ ] Optimize database queries
- [ ] Enable Gunicorn worker tuning
- [ ] Set up CDN for static files

### Frontend
- [ ] Enable Next.js caching
- [ ] Optimize images
- [ ] Enable compression
- [ ] Configure CDN
- [ ] Minimize bundle size

### Infrastructure
- [ ] Tune Nginx configuration
- [ ] Configure proper resource limits
- [ ] Set up horizontal pod autoscaling
- [ ] Enable persistent volumes
- [ ] Configure network policies

## Security Hardening

- [ ] Enable HTTPS only
- [ ] Configure security headers
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable rate limiting
- [ ] Configure DDoS protection
- [ ] Set up intrusion detection
- [ ] Enable audit logging
- [ ] Configure RBAC for Kubernetes
- [ ] Scan images for vulnerabilities
- [ ] Set up secrets rotation

## Documentation

- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document backup/restore procedures
- [ ] Create incident response plan
- [ ] Document scaling procedures
- [ ] Update API documentation
- [ ] Create user guides

## Training

- [ ] Train operations team
- [ ] Train support team
- [ ] Create admin user guide
- [ ] Create officer user guide
- [ ] Document troubleshooting steps

## Go-Live

- [ ] Schedule maintenance window
- [ ] Notify users of launch
- [ ] Monitor closely for first 24 hours
- [ ] Have rollback plan ready
- [ ] Keep team on standby

## Post-Launch

- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Review logs for issues
- [ ] Gather user feedback
- [ ] Plan optimization iterations

---

**Remember**: Always test in staging environment before production deployment!
