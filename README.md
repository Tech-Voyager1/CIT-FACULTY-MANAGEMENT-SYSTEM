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

1. **Python 3.8+** installed on your system.
2. **MySQL Server 8.0+** running locally (Port 3306).

---

## Setup Instructions

### 1. Install Dependencies
Open terminal/PowerShell in the project directory and run:
```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials
Copy `.env.example` to `.env` and fill in your local MySQL root password:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=cit_faculty_db
```
*(Note: You can also configure your password directly inside the app using the **⚙️ DB Config** button).*

### 3. Initialize Database Schema and Load Seed Data
You can either run the Python auto-initializer or execute the SQL scripts directly in MySQL Workbench / Command Line:

**Option A (Automated):**
Running `main.py` automatically creates `cit_faculty_db` and executes `schema.sql` and `seed.sql` on first launch!

**Option B (Manual via MySQL CLI):**
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql
```

---

## Running the Application

Launch the desktop application by running:
```bash
python main.py
```

---

## Project Structure

```
CIT_Faculty_Management/
├── main.py                    # Tkinter GUI Main Application Window & Dialogs
├── db.py                      # Database helper module & MySQL connector logic
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
