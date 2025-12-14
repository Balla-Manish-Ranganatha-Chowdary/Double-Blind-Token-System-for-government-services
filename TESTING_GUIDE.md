# Testing Guide - Government Portal

Complete guide for testing the Government Portal system after bug fixes.

## Prerequisites

1. **Install Dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Setup Database**:
```bash
python manage.py makemigrations
python manage.py migrate
python setup_db.py
```

3. **Generate Keys** (if not done):
```bash
python generate_keys.py
# Copy keys to .env file
```

---

## Unit Testing

### Run All Tests
```bash
cd backend

# Run all tests with verbose output
python manage.py test --verbosity=2

# Or use the test script
cd ..
test_system.bat  # Windows
```

### Run Specific Test Suites
```bash
# Encryption tests
python manage.py test apps.encryption.tests -v 2

# Officer tests
python manage.py test apps.officers.tests -v 2

# Application tests
python manage.py test apps.applications.tests -v 2

# AI services tests
python manage.py test apps.ai_services.tests -v 2
```

### Expected Results
```
Ran 36 tests in X.XXXs
OK
```

---

## Integration Testing

### 1. Test Encryption Service

**Python Shell**:
```bash
python manage.py shell
```

```python
from apps.encryption.services import EncryptionService

# Initialize service
service = EncryptionService()

# Test TE1 generation
te1 = service.generate_te1_token("APP123")
print(f"TE1: {te1}")

# Test TE2 generation
te2 = service.generate_te2_token(te1)
print(f"TE2: {te2}")

# Test decryption
decrypted_te1 = service.decrypt_te2_token(te2)
print(f"Decrypted TE1: {decrypted_te1}")
print(f"Match: {decrypted_te1 == te1}")

# Test full decryption
original = service.full_decrypt(te2)
print(f"Original: {original}")
print(f"Match: {original == 'APP123'}")
```

**Expected Output**:
```
TE1: gAAAAABl...
TE2: gAAAAABl...
Decrypted TE1: gAAAAABl...
Match: True
Original: APP123
Match: True
```

---

### 2. Test Officer Assignment

**Python Shell**:
```python
from apps.officers.models import Officer
from apps.applications.models import Application
from apps.officers.assignment import OfficerAssignmentAlgorithm
from django.contrib.auth.models import User

# Create test officer
user = User.objects.create_user(username='test_officer', password='test123')
officer = Officer.objects.create(
    user=user,
    department='REVENUE',
    hierarchy_level=1,
    is_active=True,
    workload_count=0
)

# Create test application
app = Application.objects.create(
    applicant_name="Test User",
    applicant_email="test@example.com",
    service_category="LAND_RECORD",
    status="CLASSIFIED"
)

# Test assignment
algorithm = OfficerAssignmentAlgorithm()
assigned_officer = algorithm.assign_officer(app)

print(f"Assigned Officer: {assigned_officer.user.username}")
print(f"Department: {assigned_officer.department}")
print(f"Workload: {assigned_officer.workload_count}")
print(f"Application Status: {app.status}")
```

**Expected Output**:
```
Assigned Officer: test_officer
Department: REVENUE
Workload: 1
Application Status: ASSIGNED
```

---

### 3. Test Health Check Endpoint

**Start Server**:
```bash
python manage.py runserver
```

**Test with curl**:
```bash
curl http://localhost:8000/api/analytics/health/
```

**Expected Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "not_configured"
}
```

**Test with Python**:
```python
import requests

response = requests.get('http://localhost:8000/api/analytics/health/')
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

---

### 4. Test Application Submission

**Create test PDF** (without PII):
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Land Record Application")
    c.drawString(100, 730, "Request for property survey document")
    c.drawString(100, 710, "Plot number: 123/456")
    c.drawString(100, 690, "Survey area: 2 acres")
    c.save()

create_test_pdf("test_application.pdf")
```

**Submit via API**:
```python
import requests

url = 'http://localhost:8000/api/applications/submit/'
files = {'document': open('test_application.pdf', 'rb')}
data = {
    'applicant_name': 'Test User',
    'applicant_email': 'test@example.com',
    'applicant_phone': '9876543210',
    'description': 'Land record request'
}

response = requests.post(url, data=data, files=files)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

---

### 5. Test Classification

**Python Shell**:
```python
from apps.ai_services.classification import AgenticServiceClassifier

classifier = AgenticServiceClassifier()

# Test with text
test_text = "I need a land record certificate for my property survey"
result = classifier._router_classify(test_text)

print(f"Category: {result['category']}")
print(f"Confidence: {result['confidence']}")
```

**Expected Output**:
```
Category: LAND_RECORD
Confidence: 0.8
```

---

### 6. Test PII Detection

**Python Shell**:
```python
from apps.ai_services.redaction import AgenticPIIDetector

detector = AgenticPIIDetector()

# Test with PII
text_with_pii = "Contact me at 9876543210 or john@example.com"
result = detector._router_detect(text_with_pii)

print(f"Has PII: {result['has_pii']}")
print(f"PII Types: {result['pii_types']}")

# Test without PII
text_without_pii = "This is a general application for certificate"
result = detector._router_detect(text_without_pii)

print(f"Has PII: {result['has_pii']}")
```

**Expected Output**:
```
Has PII: True
PII Types: [{'type': 'phone', 'count': 1, ...}, {'type': 'email', 'count': 1, ...}]
Has PII: False
```

---

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

### Run Load Test
```bash
# Basic test
k6 run loadtest.js

# Heavy load
k6 run --vus 100 --duration 5m loadtest.js
```

### Expected Results
```
✓ homepage status is 200
✓ health check status is 200
✓ health check is healthy

checks.........................: 100.00%
http_req_duration..............: avg=150ms p(95)=300ms
http_req_failed................: 0.00%
```

---

## Docker Testing

### Build and Start
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### Test Services
```bash
# Test backend health
curl http://localhost/api/analytics/health/

# Test frontend
curl http://localhost/

# Check logs
docker-compose logs -f backend
```

### Run Migrations in Docker
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python setup_db.py
```

---

## Kubernetes Testing

### Deploy to K8s
```bash
# Apply all manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n gov-portal
kubectl get svc -n gov-portal
kubectl get hpa -n gov-portal
```

### Test in K8s
```bash
# Port forward to test
kubectl port-forward svc/backend-service 8000:8000 -n gov-portal

# Test health check
curl http://localhost:8000/api/health/

# Check logs
kubectl logs -f <pod-name> -n gov-portal
```

---

## End-to-End Testing

### Complete Workflow Test

1. **Submit Application**:
```bash
curl -X POST http://localhost:8000/api/applications/submit/ \
  -F "applicant_name=Test User" \
  -F "applicant_email=test@example.com" \
  -F "applicant_phone=9876543210" \
  -F "description=Land record request" \
  -F "document=@test_application.pdf"
```

2. **Get Token from Response**:
```json
{
  "token": "gAAAAABl...",
  "message": "Application submitted successfully"
}
```

3. **Check Status**:
```bash
curl http://localhost:8000/api/applications/status/?token=gAAAAABl...
```

4. **Officer Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "officer_revenue_1", "password": "officer123"}'
```

5. **View Assigned Applications**:
```bash
curl http://localhost:8000/api/officers/applications/ \
  -H "Authorization: Token <auth-token>"
```

6. **Approve Application**:
```bash
curl -X POST http://localhost:8000/api/applications/<id>/approve/ \
  -H "Authorization: Token <auth-token>"
```

---

## Performance Testing

### Metrics to Monitor

1. **Response Time**:
   - Health check: < 100ms
   - Application submission: < 2s
   - Status check: < 500ms

2. **Throughput**:
   - Concurrent users: 100+
   - Requests per second: 50+

3. **Resource Usage**:
   - CPU: < 70%
   - Memory: < 80%
   - Database connections: < 100

### Monitoring Commands
```bash
# Docker stats
docker stats

# Kubernetes metrics
kubectl top pods -n gov-portal
kubectl top nodes

# Database connections
docker-compose exec postgres-primary psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

---

## Troubleshooting

### Tests Failing

**Issue**: ImportError: No module named 'django'
**Fix**: 
```bash
pip install -r requirements.txt
```

**Issue**: Database connection error
**Fix**:
```bash
# Check database is running
docker-compose ps postgres-primary

# Run migrations
python manage.py migrate
```

### Health Check Failing

**Issue**: Database not connected
**Fix**:
```bash
# Check database settings in .env
# Ensure DB_HOST, DB_PORT are correct
```

**Issue**: Redis unavailable
**Fix**: This is OK - health check should still return 200

### Assignment Not Working

**Issue**: No officers found
**Fix**:
```bash
# Run setup script to create officers
python setup_db.py
```

---

## Test Coverage

### Current Coverage

- ✅ Encryption: 9 tests
- ✅ Officers: 7 tests
- ✅ Applications: 8 tests
- ✅ AI Services: 12 tests
- **Total**: 36 unit tests

### To Add

- [ ] Integration tests for full workflow
- [ ] API endpoint tests with authentication
- [ ] Frontend component tests
- [ ] E2E tests with Selenium/Playwright

---

## Success Criteria

System is ready for deployment when:

- [x] All unit tests pass
- [x] Health check returns 200
- [x] Application submission works
- [x] Officer assignment works
- [x] Status check works
- [x] Docker containers start
- [x] Load test passes
- [ ] E2E workflow completes
- [ ] No errors in logs

---

**Testing complete! System is ready for staging deployment.**
