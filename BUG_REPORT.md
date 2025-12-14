# Bug Report & Fixes - Government Portal

## Critical Bugs Found

### 1. ❌ Encryption Service Class Name Mismatch
**Location**: `backend/apps/encryption/services.py`
**Issue**: Class is named `TokenEncryptionService` but tests expect `EncryptionService`
**Impact**: HIGH - Tests will fail, API calls may fail
**Status**: NEEDS FIX

**Current Code**:
```python
class TokenEncryptionService:
```

**Expected**:
```python
class EncryptionService:
```

**Fix**: Rename class or add alias

---

### 2. ❌ Encryption Key Encoding Issue
**Location**: `backend/apps/encryption/services.py`
**Issue**: Keys are already base64 encoded strings, encoding again causes errors
**Impact**: HIGH - Encryption will fail
**Status**: NEEDS FIX

**Current Code**:
```python
self.cipher_te1 = Fernet(settings.ENCRYPTION_KEY.encode() if settings.ENCRYPTION_KEY else Fernet.generate_key())
```

**Problem**: `settings.ENCRYPTION_KEY` is already a base64 string like `"NmwhLfg17m48JFJWwjy_WuLgKWHRaiXINcRS4VTsRcw="`
Calling `.encode()` on it creates `b'NmwhLfg17m48JFJWwjy_WuLgKWHRaiXINcRS4VTsRcw='` which is invalid for Fernet

**Fix**: Remove `.encode()` or ensure keys are bytes

---

### 3. ❌ Missing Method in Encryption Service
**Location**: `backend/apps/encryption/services.py`
**Issue**: Tests expect methods `generate_te1_token()` and `generate_te2_token()` but service has different method names
**Impact**: HIGH - API integration broken
**Status**: NEEDS FIX

**Expected Methods**:
- `generate_te1_token(data)`
- `generate_te2_token(te1_token)`
- `decrypt_te1_token(te1_token)`
- `decrypt_te2_token(te2_token)`

**Current Methods**:
- `encrypt_te1(token)`
- `encrypt_te2(token)`
- `decrypt_te1(te1_token)`
- `decrypt_te2(te2_token)`

---

### 4. ⚠️ Assignment Algorithm Department Mismatch
**Location**: `backend/apps/officers/assignment.py`
**Issue**: Service categories don't match officer departments
**Impact**: MEDIUM - Officers won't be assigned correctly
**Status**: NEEDS FIX

**Problem**:
- Service categories: `LAND_RECORD`, `POLICE_VERIFICATION`, etc.
- Officer departments: `REVENUE`, `HEALTH`, `EDUCATION`, etc.
- Mapping returns: `Revenue`, `Police`, `Civil Supplies` (different case/names)

**Fix**: Standardize department names across system

---

### 5. ⚠️ PII Detection False Positives
**Location**: `backend/apps/ai_services/redaction.py`
**Issue**: Name pattern `\b[A-Z][a-z]+\s+[A-Z][a-z]+\b` will match any capitalized words
**Impact**: MEDIUM - Will reject valid documents
**Status**: NEEDS IMPROVEMENT

**Example False Positives**:
- "New Delhi" (city name)
- "Supreme Court" (institution)
- "Income Tax" (service name)

**Fix**: Add context-aware validation or whitelist

---

### 6. ⚠️ Classification Confidence Calculation
**Location**: `backend/apps/ai_services/classification.py`
**Issue**: Confidence boost logic may exceed 1.0
**Impact**: LOW - Incorrect confidence scores
**Status**: NEEDS FIX

**Current Code**:
```python
score = min(best_score * 1.2, 1.0)  # Boost score slightly
```

**Problem**: If `best_score = 0.9`, result is `1.08` before min(), which is capped at 1.0
This is correct, but the boost factor of 1.2 is arbitrary

---

### 7. ❌ Missing URL Configuration
**Location**: `backend/apps/analytics/urls.py`
**Issue**: Created new URL file but not included in main `config/urls.py`
**Impact**: HIGH - Health check endpoint won't work
**Status**: NEEDS FIX

**Fix**: Add to `config/urls.py`:
```python
path('api/analytics/', include('apps.analytics.urls')),
```

---

### 8. ⚠️ Redis Connection in Health Check
**Location**: `backend/apps/analytics/views.py`
**Issue**: Health check tries to connect to Redis but may fail if Redis not configured
**Impact**: MEDIUM - Health check will show unhealthy even if app works
**Status**: NEEDS IMPROVEMENT

**Current Code**:
```python
redis_url = settings.CACHES['default']['LOCATION']
r = redis.from_url(redis_url)
r.ping()
```

**Problem**: If Redis is not configured or down, health check fails
**Fix**: Make Redis check optional or handle gracefully

---

### 9. ⚠️ Celery Configuration Missing
**Location**: `backend/config/__init__.py`
**Issue**: Celery app imported but may not be initialized properly
**Impact**: MEDIUM - Async tasks may not work
**Status**: NEEDS VERIFICATION

**Current Code**:
```python
from .celery import app as celery_app
__all__ = ('celery_app',)
```

**Potential Issue**: If celery.py has errors, entire app won't start
**Fix**: Add error handling or make celery optional

---

### 10. ⚠️ Docker Compose Port Conflict
**Location**: `docker-compose.yml`
**Issue**: Grafana configured on port 3001 but frontend on 3000
**Impact**: LOW - Port conflict if frontend runs outside Docker
**Status**: ACCEPTABLE (by design)

**Note**: This is intentional to avoid conflicts, but should be documented

---

## Non-Critical Issues

### 11. 📝 Missing Database Migrations
**Location**: `backend/apps/*/migrations/`
**Issue**: No migration files created yet
**Impact**: LOW - Need to run `makemigrations` before deployment
**Status**: EXPECTED (normal workflow)

---

### 12. 📝 Test Dependencies Not Installed
**Location**: Tests fail because Django not installed
**Issue**: Virtual environment not activated or dependencies not installed
**Impact**: LOW - Expected in fresh setup
**Status**: EXPECTED (user needs to install)

---

### 13. 📝 Frontend Environment Variables
**Location**: `frontend/.env.local.example`
**Issue**: Example file exists but actual `.env.local` not created
**Impact**: LOW - Frontend API calls may fail
**Status**: EXPECTED (user needs to create)

---

## Recommendations

### High Priority Fixes

1. **Fix Encryption Service** (Critical)
   - Rename class to `EncryptionService`
   - Fix key encoding issue
   - Align method names with expected interface

2. **Fix URL Configuration** (Critical)
   - Add analytics URLs to main config
   - Test health check endpoint

3. **Standardize Department Names** (High)
   - Create constants file for departments
   - Update all references to use constants

### Medium Priority Improvements

4. **Improve PII Detection** (Medium)
   - Add whitelist for common false positives
   - Improve name detection context awareness

5. **Make Redis Optional** (Medium)
   - Add graceful fallback if Redis not available
   - Update health check to handle missing Redis

6. **Add Error Handling** (Medium)
   - Add try-catch blocks in critical paths
   - Return meaningful error messages

### Low Priority Enhancements

7. **Add Logging** (Low)
   - Add structured logging throughout
   - Log classification decisions
   - Log assignment decisions

8. **Add Metrics** (Low)
   - Add Prometheus metrics
   - Track classification accuracy
   - Track assignment distribution

9. **Documentation** (Low)
   - Document all API endpoints
   - Add inline code comments
   - Create troubleshooting guide

---

## Testing Checklist

Before deployment, verify:

- [ ] Encryption service works end-to-end
- [ ] Application submission creates tokens correctly
- [ ] Status check retrieves application by token
- [ ] Officer assignment distributes workload evenly
- [ ] Classification categorizes documents correctly
- [ ] PII detection catches sensitive information
- [ ] Health check endpoint returns 200
- [ ] Docker containers start successfully
- [ ] Kubernetes pods deploy without errors
- [ ] Load balancer routes traffic correctly

---

## Next Steps

1. Apply critical fixes (items 1-3)
2. Run unit tests to verify fixes
3. Test integration end-to-end
4. Apply medium priority improvements
5. Deploy to staging for testing
6. Monitor for additional issues
