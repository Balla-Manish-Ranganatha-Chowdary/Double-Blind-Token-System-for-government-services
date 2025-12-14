# Complete Setup Instructions

## Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 15 or higher

## Step 1: Database Setup

1. Install PostgreSQL and create database:
```sql
CREATE DATABASE gov_services_db;
CREATE USER gov_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE gov_services_db TO gov_user;
```

## Step 2: Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Generate encryption keys:
```bash
python generate_keys.py
```

5. Create `.env` file (copy from `.env.example`):
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

6. Edit `.env` file with your settings:
- Add database credentials
- Add the encryption keys from step 4
- Set SECRET_KEY (use Django's get_random_secret_key())

7. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

8. Create initial data:
```bash
python setup_db.py
```

9. Start backend server:
```bash
python manage.py runserver
```

Backend will run on: http://localhost:8000

## Step 3: Frontend Setup

1. Open new terminal and navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```bash
copy .env.local.example .env.local  # Windows
cp .env.local.example .env.local    # Linux/Mac
```

4. Start frontend server:
```bash
npm run dev
```

Frontend will run on: http://localhost:3000

## Step 4: Access the Application

### Citizen Portal
- URL: http://localhost:3000
- No login required
- Apply for services and track status

### Officer Portal
- URL: http://localhost:3000/officer/login
- Sample credentials:
  - Username: `officer_revenue_1`
  - Password: `officer123`

### Admin Portal
- URL: http://localhost:3000/admin/login
- Credentials:
  - Username: `admin`
  - Password: `admin123`

## Testing the System

1. **Submit Application (Citizen)**:
   - Go to http://localhost:3000/apply
   - Fill in details (name, age, address, Aadhaar)
   - Upload PDF documents (ensure no personal info in PDFs)
   - Submit and save the token

2. **Review Application (Officer)**:
   - Login at http://localhost:3000/officer/login
   - View assigned applications
   - Approve or reject

3. **Check Status (Citizen)**:
   - Go to http://localhost:3000/status
   - Enter your token
   - View application status

4. **Manage System (Admin)**:
   - Login at http://localhost:3000/admin/login
   - View analytics dashboard
   - Manage officers (add/remove/deactivate)

## Important Notes

1. **Document Requirements**: 
   - PDFs must NOT contain applicant's name, Aadhaar, or phone numbers
   - AI will auto-reject applications with personal identifiers

2. **Security**:
   - Never commit `.env` files
   - Keep encryption keys secure
   - Change default passwords in production

3. **Production Deployment**:
   - Set DEBUG=False
   - Use strong SECRET_KEY
   - Configure proper ALLOWED_HOSTS
   - Use production database credentials
   - Set up HTTPS
   - Configure proper CORS settings

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

### Import Errors
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

### Frontend API Errors
- Ensure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in `.env.local`
- Verify CORS settings in Django

### Token Authentication Issues
- Run migrations: `python manage.py migrate`
- Ensure `rest_framework.authtoken` is in INSTALLED_APPS
