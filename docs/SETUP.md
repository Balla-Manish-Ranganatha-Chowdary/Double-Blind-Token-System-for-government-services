# Setup Guide

## Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+

## Backend Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE gov_services_db;
```

2. Navigate to backend:
```bash
cd backend
```

3. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Generate encryption keys:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())  # Run twice for two keys
```

6. Create `.env` file from `.env.example` and add keys

7. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

8. Create superuser:
```bash
python manage.py createsuperuser
```

9. Start server:
```bash
python manage.py runserver
```

## Frontend Setup

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` from `.env.local.example`

4. Start development server:
```bash
npm run dev
```

## Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin Panel: http://localhost:8000/admin
