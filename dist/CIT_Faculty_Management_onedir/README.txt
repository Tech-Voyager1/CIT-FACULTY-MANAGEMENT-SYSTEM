============================================================
CIT FACULTY MANAGEMENT SYSTEM - WINDOWS APPLICATION
Course: 23EC523 DBMS Laboratory
============================================================

PREREQUISITES:
- MySQL Server 8.0 or higher running locally on port 3306.
- (Python is NOT required to run this executable).

------------------------------------------------------------
STEP-BY-STEP SETUP INSTRUCTIONS:
------------------------------------------------------------

1. INSTALL MYSQL SERVER:
   If not already installed, download and install MySQL Community Server:
   https://dev.mysql.com/downloads/installer/
   Set port to 3306 and set a root password.

2. START MYSQL SERVICE:
   Ensure the MySQL service is running (Services -> MySQL80).

3. CONFIGURE .env:
   Copy .env.example to .env:
     - Duplicate '.env.example' and rename the copy to '.env'
     - Open '.env' in Notepad and enter your MySQL root password:
         DB_HOST=localhost
         DB_PORT=3306
         DB_USER=root
         DB_PASSWORD=your_actual_mysql_password
         DB_NAME=cit_faculty_db

4. INITIALIZE THE DATABASE (schema.sql & seed.sql):
   Open Command Prompt in this folder and run:
     mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS cit_faculty_db;"
     mysql -u root -p cit_faculty_db < database\schema.sql
     mysql -u root -p cit_faculty_db < database\seed.sql

5. LAUNCH THE APPLICATION:
   Double-click CIT_Faculty_Management.exe to start the system.

------------------------------------------------------------
TROUBLESHOOTING:
------------------------------------------------------------
- "MySQL server could not be reached":
  1. Verify the MySQL service is running.
  2. Check that the DB_PASSWORD in .env matches your MySQL root password.
  3. You can also configure credentials directly inside the app using the
     DB Config button.
