# Quick Reference Guide

## 🚀 Start the Application

### Backend
```bash
cd backend
venv\Scripts\activate  # Windows
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm run dev
```

## 🔑 Default Credentials

### Admin
- URL: http://localhost:3000/admin/login
- Username: `admin`
- Password: `admin123`

### Sample Officers
- URL: http://localhost:3000/officer/login
- Username: `officer_revenue_1` | Password: `officer123`
- Username: `officer_police_1` | Password: `officer123`
- Username: `officer_transport_1` | Password: `officer123`

### Citizens
- No login required
- Access: http://localhost:3000

## 📍 Important URLs

| Portal | URL |
|--------|-----|
| Home | http://localhost:3000 |
| Apply | http://localhost:3000/apply |
| Check Status | http://localhost:3000/status |
| Officer Login | http://localhost:3000/officer/login |
| Officer Dashboard | http://localhost:3000/officer/dashboard |
| Admin Login | http://localhost:3000/admin/login |
| Admin Dashboard | http://localhost:3000/admin/dashboard |
| Manage Officers | http://localhost:3000/admin/officers |
| Django Admin | http://localhost:8000/admin |
| API Root | http://localhost:8000/api |

## 🔧 Common Commands

### Backend Commands
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Create sample data
python setup_db.py

# Generate encryption keys
python generate_keys.py

# Django shell
python manage.py shell
```

### Frontend Commands
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## 📊 Service Categories

| Category | Department | Example Use Cases |
|----------|-----------|-------------------|
| LAND_RECORD | Revenue | Property records, land surveys |
| POLICE_VERIFICATION | Police | Background checks, clearances |
| RATION_CARD | Civil Supplies | Food security cards |
| VEHICLE_REGISTRATION | Transport | RC, driving license |
| BUILDING_PERMISSION | Municipal | Construction permits |
| REVENUE_MUTATION | Revenue | Property transfers |

## 🔐 Encryption Keys

Generate new keys:
```bash
cd backend
python generate_keys.py
```

Add to `.env`:
```
ENCRYPTION_KEY=your_key_here
ENCRYPTION_KEY_SECONDARY=your_second_key_here
```

## 🗄️ Database Quick Access

### PostgreSQL Commands
```bash
# Connect to database
psql -U postgres -d gov_services_db

# List tables
\dt

# View applications
SELECT id, service_category, status FROM applications;

# View officers
SELECT u.username, o.department, o.hierarchy_level, o.workload_count 
FROM officers o 
JOIN auth_user u ON o.user_id = u.id;

# Exit
\q
```

## 🧪 Testing Workflow

### 1. Test Application Submission
```
1. Go to http://localhost:3000/apply
2. Fill form: Name, Age, Address, Aadhaar
3. Upload PDF (without personal info)
4. Submit
5. Save the token displayed
```

### 2. Test Status Check
```
1. Go to http://localhost:3000/status
2. Enter saved token
3. View application status
```

### 3. Test Officer Review
```
1. Login at http://localhost:3000/officer/login
2. View assigned applications
3. Click on application to expand
4. Click Approve or Reject
```

### 4. Test Admin Functions
```
1. Login at http://localhost:3000/admin/login
2. View analytics dashboard
3. Go to Manage Officers
4. Add new officer
5. View officer list
```

## 🐛 Troubleshooting

### Backend Issues

**Database connection error**
```bash
# Check PostgreSQL is running
# Verify credentials in .env
# Ensure database exists
```

**Import errors**
```bash
# Activate virtual environment
venv\Scripts\activate
# Reinstall requirements
pip install -r requirements.txt
```

**Migration errors**
```bash
# Delete migrations (except __init__.py)
# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

### Frontend Issues

**API connection error**
```bash
# Check backend is running on port 8000
# Verify NEXT_PUBLIC_API_URL in .env.local
# Check CORS settings in Django
```

**Module not found**
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

**Build errors**
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

## 📝 Environment Variables

### Backend (.env)
```
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=gov_services_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

ENCRYPTION_KEY=your_fernet_key_1
ENCRYPTION_KEY_SECONDARY=your_fernet_key_2
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 🔄 Application Status Flow

```
SUBMITTED → CLASSIFIED → REDACTION_CLEARED → ASSIGNED → 
IN_REVIEW → FORWARDED (if multi-level) → APPROVED/REJECTED
```

## 📞 API Quick Reference

### Public Endpoints
```bash
# Submit application
POST /api/applications/submit/
Content-Type: multipart/form-data

# Check status
GET /api/applications/status/{token}/
```

### Officer Endpoints (Auth Required)
```bash
# List assigned applications
GET /api/applications/officer/list/
Authorization: Token {your_token}

# Approve/Reject
POST /api/applications/officer/action/{id}/
Authorization: Token {your_token}
Body: {"action": "APPROVE"} or {"action": "REJECT"}
```

### Admin Endpoints (Admin Auth Required)
```bash
# Analytics
GET /api/analytics/dashboard/
Authorization: Token {admin_token}

# List officers
GET /api/officers/
Authorization: Token {admin_token}

# Create officer
POST /api/officers/create/
Authorization: Token {admin_token}
Body: {
  "username": "officer_name",
  "password": "password",
  "department": "Revenue",
  "hierarchy_level": 1
}
```

## 💡 Tips

1. **Always check backend logs** when debugging API issues
2. **Use Django admin** (http://localhost:8000/admin) for direct database access
3. **Clear browser cache** if seeing stale data
4. **Check browser console** for frontend errors
5. **Verify tokens** are being stored in localStorage
6. **Test with clean PDFs** (no personal info) first
7. **Monitor officer workload** in admin dashboard

## 📚 Additional Resources

- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Detailed setup
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Complete documentation
- [FUNCTIONALITY_CHECKLIST.md](FUNCTIONALITY_CHECKLIST.md) - Feature verification
- [docs/API.md](docs/API.md) - API documentation
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
