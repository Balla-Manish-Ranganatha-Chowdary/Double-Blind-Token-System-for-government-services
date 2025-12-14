# PostgreSQL Database Setup Guide

## Option 1: Using Command Line (Recommended)

### Windows

1. **Open Command Prompt as Administrator**

2. **Navigate to PostgreSQL bin directory** (adjust path based on your installation):
```cmd
cd "C:\Program Files\PostgreSQL\15\bin"
```

3. **Connect to PostgreSQL**:
```cmd
psql -U postgres
```

4. **Enter your PostgreSQL password when prompted**

5. **Create the database**:
```sql
CREATE DATABASE gov_services_db;
```

6. **Verify database was created**:
```sql
\l
```

7. **Exit psql**:
```sql
\q
```

### Alternative: Run SQL Script

```cmd
psql -U postgres -f path\to\setup_database.sql
```

## Option 2: Using pgAdmin (GUI)

1. **Open pgAdmin 4**

2. **Connect to your PostgreSQL server**
   - Right-click on "PostgreSQL 15" (or your version)
   - Enter your password

3. **Create Database**
   - Right-click on "Databases"
   - Select "Create" → "Database..."
   - Database name: `gov_services_db`
   - Owner: `postgres` (or your user)
   - Click "Save"

4. **Verify**
   - You should see `gov_services_db` in the database list

## Option 3: Using SQL Shell (psql)

1. **Open SQL Shell (psql)** from Start Menu

2. **Press Enter for defaults** until you reach password prompt:
   - Server: localhost
   - Database: postgres
   - Port: 5432
   - Username: postgres

3. **Enter your password**

4. **Create database**:
```sql
CREATE DATABASE gov_services_db;
```

5. **Verify**:
```sql
\l
```

## Verify Database Setup

After creating the database, verify it exists:

```sql
-- List all databases
\l

-- Connect to the database
\c gov_services_db

-- Check current database
SELECT current_database();
```

You should see `gov_services_db` in the output.

## Configure Backend Connection

After creating the database, update your `backend/.env` file:

```env
DB_NAME=gov_services_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

## Troubleshooting

### "psql: command not found"
- Add PostgreSQL bin directory to your PATH
- Or use full path: `"C:\Program Files\PostgreSQL\15\bin\psql"`

### "password authentication failed"
- Verify your PostgreSQL password
- Check if PostgreSQL service is running

### "database already exists"
- Database is already created, you're good to go!
- Or drop and recreate: `DROP DATABASE gov_services_db;`

### Check if PostgreSQL is running

**Windows:**
```cmd
# Check service status
sc query postgresql-x64-15

# Start service if not running
net start postgresql-x64-15
```

**Services GUI:**
- Press `Win + R`, type `services.msc`
- Find "postgresql-x64-15" (or your version)
- Ensure it's "Running"

## Next Steps

Once database is created:

1. ✅ Database created
2. ⏭️ Configure backend `.env` file
3. ⏭️ Run migrations: `python manage.py migrate`
4. ⏭️ Create initial data: `python setup_db.py`

## Quick Test

Test database connection:

```cmd
cd backend
python manage.py dbshell
```

If it connects successfully, your database is ready!
