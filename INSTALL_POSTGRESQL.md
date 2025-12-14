# PostgreSQL Installation Guide for Windows

## Step 1: Download PostgreSQL

1. Go to: https://www.postgresql.org/download/windows/
2. Click "Download the installer"
3. Download PostgreSQL 15 or 16 (recommended)
4. Choose Windows x86-64 version

**Direct Link:** https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

## Step 2: Install PostgreSQL

1. **Run the installer** (postgresql-15.x-windows-x64.exe)

2. **Installation wizard steps:**
   - Click "Next"
   - Installation Directory: Keep default (`C:\Program Files\PostgreSQL\15`)
   - Select Components: Check all (PostgreSQL Server, pgAdmin 4, Command Line Tools)
   - Data Directory: Keep default
   - **Password:** Enter a password for postgres user (REMEMBER THIS!)
   - Port: Keep default (5432)
   - Locale: Keep default
   - Click "Next" and "Install"

3. **Wait for installation** (may take 5-10 minutes)

4. **Uncheck "Stack Builder"** at the end (not needed)

5. **Click "Finish"**

## Step 3: Verify Installation

### Option A: Using pgAdmin 4

1. Open **pgAdmin 4** from Start Menu
2. Set a master password (for pgAdmin itself)
3. Expand "Servers" → "PostgreSQL 15"
4. Enter the password you set during installation
5. If you see the server dashboard, PostgreSQL is installed correctly!

### Option B: Using Command Line

1. Open **Command Prompt**

2. Navigate to PostgreSQL bin:
```cmd
cd "C:\Program Files\PostgreSQL\15\bin"
```

3. Test connection:
```cmd
psql -U postgres
```

4. Enter your password

5. If you see `postgres=#` prompt, it's working!

6. Type `\q` to exit

## Step 4: Add PostgreSQL to PATH (Optional but Recommended)

This allows you to run `psql` from anywhere:

1. Press `Win + X` → Select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find "Path"
5. Click "Edit"
6. Click "New"
7. Add: `C:\Program Files\PostgreSQL\15\bin`
8. Click "OK" on all windows
9. **Restart Command Prompt** for changes to take effect

## Step 5: Create Database for Project

### Method 1: Using pgAdmin 4 (Easiest)

1. Open **pgAdmin 4**
2. Connect to PostgreSQL 15 server
3. Right-click on "Databases"
4. Select "Create" → "Database..."
5. Database name: `gov_services_db`
6. Owner: `postgres`
7. Click "Save"

✅ **Done!** Database created.

### Method 2: Using SQL Shell (psql)

1. Open **SQL Shell (psql)** from Start Menu
2. Press Enter for all defaults (Server, Database, Port, Username)
3. Enter your postgres password
4. Run:
```sql
CREATE DATABASE gov_services_db;
```
5. Verify:
```sql
\l
```
6. You should see `gov_services_db` in the list

### Method 3: Using Command Prompt

1. Open Command Prompt
2. Run:
```cmd
cd "C:\Program Files\PostgreSQL\15\bin"
psql -U postgres -c "CREATE DATABASE gov_services_db;"
```
3. Enter password when prompted

## Step 6: Configure Project

1. Navigate to your project's `backend` folder

2. Create `.env` file (copy from `.env.example`):
```env
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=gov_services_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here
DB_HOST=localhost
DB_PORT=5432

ENCRYPTION_KEY=will_generate_next
ENCRYPTION_KEY_SECONDARY=will_generate_next
```

3. Replace `your_postgres_password_here` with your actual password

## Step 7: Test Database Connection

```cmd
cd backend
python manage.py dbshell
```

If it connects without errors, you're all set!

## Troubleshooting

### "psql: command not found"
- PostgreSQL not in PATH
- Use full path: `"C:\Program Files\PostgreSQL\15\bin\psql"`
- Or add to PATH (see Step 4)

### "password authentication failed"
- Wrong password
- Reset password in pgAdmin or during reinstall

### "could not connect to server"
- PostgreSQL service not running
- Open Services (Win + R → `services.msc`)
- Find "postgresql-x64-15"
- Right-click → Start

### "port 5432 already in use"
- Another PostgreSQL instance running
- Or another service using port 5432
- Change port in postgresql.conf or during installation

## Alternative: Using Docker (Advanced)

If you prefer Docker:

```bash
docker run --name postgres-gov -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15

docker exec -it postgres-gov psql -U postgres -c "CREATE DATABASE gov_services_db;"
```

## Next Steps

After PostgreSQL is installed and database is created:

1. ✅ PostgreSQL installed
2. ✅ Database `gov_services_db` created
3. ⏭️ Configure `backend/.env` file
4. ⏭️ Generate encryption keys: `python generate_keys.py`
5. ⏭️ Run migrations: `python manage.py migrate`
6. ⏭️ Create initial data: `python setup_db.py`
7. ⏭️ Start backend: `python manage.py runserver`

## Quick Reference

**Start PostgreSQL Service:**
```cmd
net start postgresql-x64-15
```

**Stop PostgreSQL Service:**
```cmd
net stop postgresql-x64-15
```

**Connect to Database:**
```cmd
psql -U postgres -d gov_services_db
```

**List Databases:**
```sql
\l
```

**List Tables:**
```sql
\dt
```

**Exit psql:**
```sql
\q
```

---

**Need help?** Check [DATABASE_SETUP.md](DATABASE_SETUP.md) for more details.
