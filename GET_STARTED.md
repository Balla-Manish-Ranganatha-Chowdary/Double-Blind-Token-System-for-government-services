# 🚀 Get Started in 5 Minutes

This guide will get your Government Services Portal up and running quickly.

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.10+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] PostgreSQL 15+ installed and running
- [ ] Git (optional, for cloning)

## Step-by-Step Setup

### 1️⃣ Database Setup (2 minutes)

Open PostgreSQL command line or pgAdmin and run:

```sql
CREATE DATABASE gov_services_db;
```

That's it for the database!

### 2️⃣ Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies (this may take a minute)
pip install -r requirements.txt

# Generate encryption keys
python generate_keys.py
```

**Copy the output keys!** You'll need them in the next step.

Create a `.env` file in the `backend` folder:

```env
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=gov_services_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

ENCRYPTION_KEY=paste_first_key_here
ENCRYPTION_KEY_SECONDARY=paste_second_key_here
```

Now run:

```bash
# Create database tables
python manage.py migrate

# Create admin and sample officers
python setup_db.py

# Start the backend server
python manage.py runserver
```

✅ Backend is now running on http://localhost:8000

### 3️⃣ Frontend Setup (1 minute)

Open a **new terminal** (keep backend running):

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > .env.local

# Start the frontend server
npm run dev
```

✅ Frontend is now running on http://localhost:3000

## 🎉 You're Done!

Open your browser and visit:

### 👤 Citizen Portal
**URL:** http://localhost:3000

Try it:
1. Click "Apply for Service"
2. Fill the form
3. Upload a PDF (make sure it doesn't contain your name or Aadhaar!)
4. Submit and save your token
5. Go to "Check Status" and enter your token

### 👮 Officer Portal
**URL:** http://localhost:3000/officer/login

Login with:
- **Username:** `officer_revenue_1`
- **Password:** `officer123`

Try it:
1. View assigned applications
2. Click on an application to expand
3. Click "Approve" or "Reject"

### 👨‍💼 Admin Portal
**URL:** http://localhost:3000/admin/login

Login with:
- **Username:** `admin`
- **Password:** `admin123`

Try it:
1. View the analytics dashboard
2. Click "Manage Officers"
3. Add a new officer
4. View officer workload

## 🐛 Something Not Working?

### Backend won't start?
```bash
# Check if PostgreSQL is running
# Check your .env file has correct database credentials
# Try: python manage.py migrate
```

### Frontend won't start?
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

### Can't login?
```bash
# Make sure you ran: python setup_db.py
# Try creating a new admin: python manage.py createsuperuser
```

### Database errors?
```bash
# Check PostgreSQL is running
# Verify database exists: psql -U postgres -l
# Check credentials in .env match your PostgreSQL setup
```

## 📚 Next Steps

Now that everything is running:

1. **Read the docs:**
   - [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Understand the system
   - [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common commands
   - [FUNCTIONALITY_CHECKLIST.md](FUNCTIONALITY_CHECKLIST.md) - All features

2. **Test the workflow:**
   - Submit an application as a citizen
   - Review it as an officer
   - Check analytics as admin

3. **Customize:**
   - Add more officers in admin panel
   - Try different service categories
   - Upload various PDF documents

## 💡 Pro Tips

- Keep both terminals open (backend + frontend)
- Use Django admin at http://localhost:8000/admin for direct database access
- Check browser console (F12) for frontend errors
- Check terminal for backend errors
- Default passwords are for development only - change them for production!

## 🎯 Quick Test Workflow

1. **Submit Application:**
   - Go to http://localhost:3000/apply
   - Name: "Test User", Age: 30, Address: "Test Address", Aadhaar: "123456789012"
   - Upload any PDF (without personal info)
   - Save the token!

2. **Check Status:**
   - Go to http://localhost:3000/status
   - Paste your token
   - See the status

3. **Officer Review:**
   - Login as officer
   - See your application (notice: no citizen name visible!)
   - Approve it

4. **Check Status Again:**
   - Go back to status page
   - Enter token
   - Status should be updated!

## 🔐 Security Note

This setup uses default credentials for development. Before deploying to production:

- [ ] Change all default passwords
- [ ] Generate new SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Use environment-specific encryption keys
- [ ] Set up HTTPS
- [ ] Configure production database

## 🆘 Need Help?

Check these files:
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Detailed setup
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Commands reference
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Complete documentation

---

**Happy coding! 🎉**
