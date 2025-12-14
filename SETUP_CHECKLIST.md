# Setup Checklist ✅

Follow this checklist to get your Government Services Portal running.

## Prerequisites

- [ ] Python 3.10+ installed
  - Check: `python --version`
  - Download: https://www.python.org/downloads/

- [ ] Node.js 18+ installed
  - Check: `node --version`
  - Download: https://nodejs.org/

- [ ] PostgreSQL 15+ installed
  - Check: `psql --version`
  - **Not installed?** → Follow [INSTALL_POSTGRESQL.md](INSTALL_POSTGRESQL.md)

## Database Setup

- [ ] PostgreSQL service is running
  - Windows: Check Services → "postgresql-x64-15" should be "Running"
  - Or run: `net start postgresql-x64-15`

- [ ] Database `gov_services_db` created
  - **Method 1 (pgAdmin):** Open pgAdmin → Create Database → Name: `gov_services_db`
  - **Method 2 (Command):** Run `setup_database.bat`
  - **Method 3 (SQL Shell):** Run `psql -U postgres -c "CREATE DATABASE gov_services_db;"`
  - Verify: `psql -U postgres -l` (should see gov_services_db in list)

## Backend Setup

- [ ] Navigate to backend folder
  ```cmd
  cd backend
  ```

- [ ] Create virtual environment
  ```cmd
  python -m venv venv
  ```

- [ ] Activate virtual environment
  ```cmd
  venv\Scripts\activate
  ```
  - You should see `(venv)` in your prompt

- [ ] Install dependencies
  ```cmd
  pip install -r requirements.txt
  ```
  - This may take 2-3 minutes

- [ ] Generate encryption keys
  ```cmd
  python generate_keys.py
  ```
  - **IMPORTANT:** Copy both keys shown

- [ ] Create `.env` file
  - Copy `.env.example` to `.env`
  - Edit `.env` and add:
    - Your PostgreSQL password
    - The two encryption keys from previous step

- [ ] Run migrations
  ```cmd
  python manage.py migrate
  ```
  - Should see "Applying..." messages

- [ ] Create initial data (admin + sample officers)
  ```cmd
  python setup_db.py
  ```
  - Should see "✓ Admin created" and "✓ Created officer_*" messages

- [ ] Start backend server
  ```cmd
  python manage.py runserver
  ```
  - Should see "Starting development server at http://127.0.0.1:8000/"
  - **Keep this terminal open!**

- [ ] Test backend (open new terminal)
  - Visit: http://localhost:8000/admin
  - Login: username=`admin`, password=`admin123`
  - If you can login, backend is working! ✅

## Frontend Setup

- [ ] Open **NEW terminal** (keep backend running)

- [ ] Navigate to frontend folder
  ```cmd
  cd frontend
  ```

- [ ] Install dependencies
  ```cmd
  npm install
  ```
  - This may take 2-3 minutes

- [ ] Create `.env.local` file
  - Copy `.env.local.example` to `.env.local`
  - Or run: `echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > .env.local`

- [ ] Start frontend server
  ```cmd
  npm run dev
  ```
  - Should see "Ready in X ms"
  - Should show "Local: http://localhost:3000"
  - **Keep this terminal open!**

- [ ] Test frontend
  - Visit: http://localhost:3000
  - Should see "Government Services Portal" homepage
  - If you see the homepage, frontend is working! ✅

## Final Verification

- [ ] Both servers running
  - Backend: http://localhost:8000 ✅
  - Frontend: http://localhost:3000 ✅

- [ ] Test citizen portal
  - Go to: http://localhost:3000/apply
  - Fill form and submit (use PDF without personal info)
  - Save the token shown

- [ ] Test status check
  - Go to: http://localhost:3000/status
  - Enter your token
  - Should show application status

- [ ] Test officer login
  - Go to: http://localhost:3000/officer/login
  - Username: `officer_revenue_1`
  - Password: `officer123`
  - Should see dashboard with applications

- [ ] Test admin login
  - Go to: http://localhost:3000/admin/login
  - Username: `admin`
  - Password: `admin123`
  - Should see analytics dashboard

## 🎉 Success!

If all checkboxes are checked, your system is fully operational!

## Common Issues

### ❌ "Database connection error"
- Check PostgreSQL is running: `net start postgresql-x64-15`
- Verify password in `backend/.env`
- Verify database exists: `psql -U postgres -l`

### ❌ "Module not found" (Backend)
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall: `pip install -r requirements.txt`

### ❌ "Cannot connect to API" (Frontend)
- Check backend is running on port 8000
- Check `.env.local` has correct API URL
- Check CORS settings in Django

### ❌ "Port already in use"
- Backend (8000): Another Django app running
- Frontend (3000): Another Next.js app running
- Kill the process or use different port

### ❌ "psql: command not found"
- PostgreSQL not in PATH
- Use full path: `"C:\Program Files\PostgreSQL\15\bin\psql"`
- Or follow Step 4 in [INSTALL_POSTGRESQL.md](INSTALL_POSTGRESQL.md)

## Need Help?

Check these guides:
- **PostgreSQL not installed?** → [INSTALL_POSTGRESQL.md](INSTALL_POSTGRESQL.md)
- **Database setup issues?** → [DATABASE_SETUP.md](DATABASE_SETUP.md)
- **Quick start guide** → [GET_STARTED.md](GET_STARTED.md)
- **Detailed setup** → [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
- **Commands reference** → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

## What's Next?

- Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) to understand the system
- Check [FUNCTIONALITY_CHECKLIST.md](FUNCTIONALITY_CHECKLIST.md) for all features
- Test the complete workflow (submit → review → approve)
- Customize officers and departments in admin panel

---

**Happy coding! 🚀**
