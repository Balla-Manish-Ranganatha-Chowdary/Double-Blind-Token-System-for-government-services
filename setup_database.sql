-- PostgreSQL Database Setup Script
-- Government Services Portal - Double-Blind Token System

-- Create database
CREATE DATABASE gov_services_db;

-- Create user (optional - you can use existing postgres user)
-- CREATE USER gov_user WITH PASSWORD 'your_secure_password';

-- Grant privileges (if you created a new user)
-- GRANT ALL PRIVILEGES ON DATABASE gov_services_db TO gov_user;

-- Connect to the database
\c gov_services_db;

-- Verify connection
SELECT current_database();

-- Show success message
SELECT 'Database gov_services_db created successfully!' AS status;
