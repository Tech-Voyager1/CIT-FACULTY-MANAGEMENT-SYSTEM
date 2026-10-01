# CIT Faculty Management System

**Course:** 23EC523 DBMS Laboratory  
**Academic Year:** 2026–27  
**Institution:** Coimbatore Institute of Technology (CIT), Coimbatore  

---

## Project Overview

The **CIT Faculty Management System** is a Python-based desktop administration system created as a DBMS Laboratory Mini-Project. The application manages faculty records across five key engineering departments at Coimbatore Institute of Technology:

1. Computer Science and Engineering (CSE)
2. Electronics and Communication Engineering (ECE)
3. Electrical and Electronics Engineering (EEE)
4. Mechanical Engineering (MECH)
5. Civil Engineering (CIVIL)

---

## Architecture

```
        +-----------------------------------+
        |       Tkinter Desktop GUI         |
        +-----------------------------------+
                          |
                          | Python-MySQL Connector (db.py)
                          v
        +-----------------------------------+
        |       MySQL Database              |
        |       (cit_faculty_db)            |
        +-----------------------------------+
               /                     \
              v                       v
     +-----------------+     +--------------------------+
     |     faculty     | <---|     faculty_academic     |
     | (Parent Table)  |  FK | (Child Table w/ CASCADE) |
     +-----------------+     +--------------------------+
```

---

## Key Features & DBMS Demonstrations

1. **Relational Database Schema (2 Related Tables):**
   - `faculty` (Parent Table with Primary Key `faculty_id`).
   - `faculty_academic` (Child Table with Primary Key `academic_id` and Foreign Key `faculty_id` `ON DELETE CASCADE`).
2. **Dashboard Summary Cards:** Real-time metrics showing overall and department-wise counts calculated via SQL `GROUP BY`.
3. **Faculty Directory (TTK Treeview):** Clean multi-column table displaying key faculty attributes.
4. **Parameterized Search:** Dynamic SQL searching using `WHERE ... LIKE %s` or `WHERE department = %s` against MySQL (no purely local filtering).
5. **Relational JOIN View:** Comprehensive profile viewer fetching data across both tables via SQL `JOIN`.
6. **Atomic Transactional CRUD:**
   - **INSERT:** Adds new faculty and academic records using a safe SQL transaction.
   - **UPDATE:** Edits information across both tables atomically.
   - **DELETE:** Deletes faculty record with automatic `ON DELETE CASCADE` removal of academic details.

---

## Prerequisites & Installation

### 1. Install Python (Version 3.8 to 3.12 Recommended)
- Download Python for Windows from [python.org/downloads](https://www.python.org/downloads/).
- **CRITICAL during installation:** Check the box **"Add Python to PATH"** before clicking Install Now.
- Verify in PowerShell / Command Prompt:
  ```bash
  python --version
  pip --version
  ```

### 2. Install MySQL Server (8.0 or Higher)
- Download MySQL Community Server or MySQL Installer from [dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/).
- Set the default port to `3306`.
- Set a strong root password during setup and remember it (e.g. `root` or `admin123`).
- Ensure the MySQL service is started (can be checked in Windows `Services.msc` -> `MySQL80`).

---

## Setup Instructions

### Step 1: Install Python Dependencies
Open PowerShell or Command Prompt inside the project folder:
```bash
pip install -r requirements.txt
```
*(Required packages: `mysql-connector-python` and `python-dotenv`).*

### Step 2: Create and Configure `.env`
Copy `.env.example` to create `.env`:
```powershell
copy .env.example .env
```
Open `.env` in any text editor and fill in your MySQL credentials:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_actual_mysql_password
DB_NAME=cit_faculty_db
```
> **Note:** Never commit `.env` containing real passwords to version control.

### Step 3: Run Database Initializer
Run the provided automated database setup script:
```bash
python setup_database.py
```
This one-step script will:
- Connect to your local MySQL server
- Create the database `cit_faculty_db` if it does not exist
- Execute `database/schema.sql` (creating `faculty` and `faculty_academic` with Foreign Key constraints)
- Execute `database/seed.sql` (populating 30 faculty members and academic credentials)
- Verify and display the imported record counts

*(Alternative manual setup via MySQL command-line client:)*
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS cit_faculty_db;"
mysql -u root -p cit_faculty_db < database/schema.sql
mysql -u root -p cit_faculty_db < database/seed.sql
```

---

## Running the Application

Launch the desktop application:
```bash
python main.py
```

---

## Troubleshooting Guide

### 1. `[ERROR] Cannot connect to MySQL: 2003: Can't connect to MySQL server`
- **Cause:** MySQL server service is not running.
- **Fix:** Press `Win + R`, type `services.msc`, locate `MySQL80` (or `MySQL`), right-click and click **Start**.

### 2. `[ERROR] 1045 (28000): Access denied for user 'root'@'localhost'`
- **Cause:** Incorrect `DB_PASSWORD` or `DB_USER` in `.env`.
- **Fix:** Double-check your MySQL root password and update the `DB_PASSWORD` value in `.env`. Alternatively, use the **⚙️ DB Config** button on the application's login/dashboard window to change credentials live.

### 3. `ModuleNotFoundError: No module named 'mysql'` or `No module named 'dotenv'`
- **Cause:** Python packages are not installed in the active environment.
- **Fix:** Run:
  ```bash
  pip install -r requirements.txt
  ```

### 4. `_tkinter.TclError` or Tkinter missing
- **Cause:** Python installed on Windows without the tcl/tk and IDLE optional feature.
- **Fix:** Re-run the Python Windows installer, choose **Modify**, and make sure **tcl/tk and IDLE** is checked.

### 5. Need to Reset Data
- To reset the entire database to the original 30 faculty records at any time, simply run:
  ```bash
  python setup_database.py
  ```

---

## Project Structure

```
CIT_Faculty_Management/
├── main.py                    # Tkinter GUI Main Application Window & Dialogs
├── setup_database.py          # One-shot database initializer & schema/seed loader
├── db.py                      # Database helper module & MySQL connector logic
├── db_logger.py               # Live SQL listener & query logger
├── .env                       # Local environment configuration file
├── .env.example               # Environment configuration template
├── requirements.txt           # Python package dependencies
├── README.md                  # Project documentation & setup guide
│
├── database/
│   ├── schema.sql             # DDL SQL script (CREATE DATABASE, TABLES, FK CASCADE)
│   ├── seed.sql               # DML SQL script (INSERT statements for 30 CIT faculty)
│   └── verification.sql       # Verification & DBMS demonstration SQL queries
│
└── data/
    ├── faculty.csv            # Approved faculty master dataset (Table 1)
    ├── faculty_academic.csv   # Approved faculty academic dataset (Table 2)
    ├── faculty_raw.json       # Raw audit JSON with source URLs
    └── data_validation_report.md # Detailed data validation & integrity report
```

---

## SQL Queries for DBMS Viva Demonstration

### 1. Relational JOIN Query
```sql
SELECT 
    f.faculty_id, f.faculty_name, f.department, f.designation,
    a.ug_qualification, a.pg_qualification, a.phd_qualification,
    a.research_interest, a.publication_count
FROM faculty f
JOIN faculty_academic a ON f.faculty_id = a.faculty_id;
```

### 2. Aggregation & Grouping Query
```sql
SELECT department, COUNT(*) AS total_faculty
FROM faculty
GROUP BY department;
```
