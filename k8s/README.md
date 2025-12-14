# Kubernetes Deployment Files

## Quick Deploy

```bash
# Windows
deploy-k8s.bat

# Linux/Mac
chmod +x deploy-k8s.sh
./deploy-k8s.sh
```

## Manual Deployment

1. **Create namespace**:
```bash
kubectl apply -f namespace.yaml
```

2. **Update secrets** in `secrets.yaml` with your values

3. **Apply configurations**:
```bash
kubectl apply -f secrets.yaml
kubectl apply -f configmap.yaml
```

4. **Deploy infrastructure**:
```bash
kubectl apply -f postgres-deployment.yaml
kubectl apply -f redis-deployment.yaml
```

5. **Deploy application**:
```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f celery-deployment.yaml
```

6. **Enable autoscaling**:
```bash
kubectl apply -f hpa.yaml
```

7. **Setup ingress**:
```bash
kubectl apply -f ingress.yaml
```

## Verify Deployment

```bash
kubectl get all -n gov-portal
kubectl get hpa -n gov-portal
kubectl get ingress -n gov-portal
```

## Scaling

### Manual Scaling
```bash
kubectl scale deployment backend --replicas=5 -n gov-portal
```

### Autoscaling (HPA)
Configured in `hpa.yaml`:
- Backend: 3-10 replicas (70% CPU)
- Frontend: 2-6 replicas (70% CPU)
- Workers: 2-8 replicas (75% CPU)

## Monitoring

```bash
# View logs
kubectl logs -f <pod-name> -n gov-portal

# Check HPA status
kubectl get hpa -n gov-portal -w

# Check resource usage
kubectl top pods -n gov-portal
```

## Troubleshooting

```bash
# Describe pod
kubectl describe pod <pod-name> -n gov-portal

# Get events
kubectl get events -n gov-portal --sort-by='.lastTimestamp'

# Restart deployment
kubectl rollout restart deployment backend -n gov-portal
```
