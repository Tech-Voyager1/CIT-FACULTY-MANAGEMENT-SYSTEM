import os
import csv

os.makedirs("database", exist_ok=True)

# 1. Read CSV files and perform integrity audits
faculty_rows = []
with open("data/faculty.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        faculty_rows.append(row)

academic_rows = []
with open("data/faculty_academic.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        academic_rows.append(row)

# Verification checks
faculty_ids = [r["faculty_id"] for r in faculty_rows]
academic_ids = [r["academic_id"] for r in academic_rows]
fk_faculty_ids = [r["faculty_id"] for r in academic_rows]

# Check uniqueness
assert len(faculty_ids) == len(set(faculty_ids)), "Duplicate faculty_id found in faculty.csv"
assert len(academic_ids) == len(set(academic_ids)), "Duplicate academic_id found in faculty_academic.csv"

# Check Foreign Key constraint (all FK references must exist in parent table)
missing_fks = [fid for fid in fk_faculty_ids if fid not in set(faculty_ids)]
assert len(missing_fks) == 0, f"Orphaned foreign keys detected: {missing_fks}"

print(f"Data Integrity Verification Passed: {len(faculty_rows)} faculty records & {len(academic_rows)} academic records.")

# Helper function to format SQL values
def sql_val(val, is_int=False):
    if val is None or val.strip() == "" or val.strip().upper() == "NULL":
        return "NULL"
    cleaned = val.replace("'", "''")
    if is_int:
        return cleaned
    return f"'{cleaned}'"

# 2. Generate database/schema.sql
schema_sql = """-- ============================================================
-- CIT FACULTY MANAGEMENT SYSTEM - DATABASE SCHEMA
-- Course: 23EC523 DBMS Laboratory (2026-27)
-- ============================================================

CREATE DATABASE IF NOT EXISTS cit_faculty_db;
USE cit_faculty_db;

-- Drop tables if existing (Child table first due to FK constraint)
DROP TABLE IF EXISTS faculty_academic;
DROP TABLE IF EXISTS faculty;

-- ------------------------------------------------------------
-- TABLE 1: faculty (Parent Table)
-- ------------------------------------------------------------
CREATE TABLE faculty (
    faculty_id VARCHAR(20) NOT NULL,
    faculty_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    email VARCHAR(100) DEFAULT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    joining_date DATE DEFAULT NULL,
    PRIMARY KEY (faculty_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- TABLE 2: faculty_academic (Child Table)
-- ------------------------------------------------------------
CREATE TABLE faculty_academic (
    academic_id VARCHAR(20) NOT NULL,
    faculty_id VARCHAR(20) NOT NULL,
    ug_qualification VARCHAR(100) DEFAULT NULL,
    pg_qualification VARCHAR(150) DEFAULT NULL,
    phd_qualification VARCHAR(150) DEFAULT NULL,
    research_interest TEXT DEFAULT NULL,
    publication_count INT DEFAULT NULL,
    PRIMARY KEY (academic_id),
    CONSTRAINT fk_faculty_academic_faculty
        FOREIGN KEY (faculty_id)
        REFERENCES faculty (faculty_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

with open("database/schema.sql", "w", encoding="utf-8") as f:
    f.write(schema_sql)

# 3. Generate database/seed.sql
seed_sql_lines = [
    "-- ============================================================",
    "-- CIT FACULTY MANAGEMENT SYSTEM - SEED DATA IMPORT",
    "-- Generated from verified data/faculty.csv & data/faculty_academic.csv",
    "-- ============================================================\n",
    "USE cit_faculty_db;\n",
    "-- Disable FK checks temporarily during bulk insert",
    "SET FOREIGN_KEY_CHECKS = 0;\n",
    "TRUNCATE TABLE faculty_academic;",
    "TRUNCATE TABLE faculty;\n",
    "SET FOREIGN_KEY_CHECKS = 1;\n",
    "-- Insert records into faculty"
]

faculty_inserts = []
for r in faculty_rows:
    fid = sql_val(r["faculty_id"])
    fname = sql_val(r["faculty_name"])
    dept = sql_val(r["department"])
    desig = sql_val(r["designation"])
    email = sql_val(r["email"])
    phone = sql_val(r["phone"])
    jdate = sql_val(r["joining_date"])
    faculty_inserts.append(f"({fid}, {fname}, {dept}, {desig}, {email}, {phone}, {jdate})")

seed_sql_lines.append(
    "INSERT INTO faculty (faculty_id, faculty_name, department, designation, email, phone, joining_date) VALUES\n" +
    ",\n".join(faculty_inserts) + ";\n"
)

seed_sql_lines.append("-- Insert records into faculty_academic")
academic_inserts = []
for r in academic_rows:
    aid = sql_val(r["academic_id"])
    fid = sql_val(r["faculty_id"])
    ug = sql_val(r["ug_qualification"])
    pg = sql_val(r["pg_qualification"])
    phd = sql_val(r["phd_qualification"])
    res = sql_val(r["research_interest"])
    pubs = sql_val(r["publication_count"], is_int=True)
    academic_inserts.append(f"({aid}, {fid}, {ug}, {pg}, {phd}, {res}, {pubs})")

seed_sql_lines.append(
    "INSERT INTO faculty_academic (academic_id, faculty_id, ug_qualification, pg_qualification, phd_qualification, research_interest, publication_count) VALUES\n" +
    ",\n".join(academic_inserts) + ";\n"
)

with open("database/seed.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(seed_sql_lines))

# 4. Generate database/verification.sql
verification_sql = """-- ============================================================
-- CIT FACULTY MANAGEMENT SYSTEM - VERIFICATION & DBMS QUERIES
-- ============================================================

USE cit_faculty_db;

-- 1. View all records from faculty master table
SELECT * FROM faculty;

-- 2. View all records from faculty_academic table
SELECT * FROM faculty_academic;

-- 3. Total count of faculty members
SELECT COUNT(*) AS total_faculty_count FROM faculty;

-- 4. Total count of academic records
SELECT COUNT(*) AS total_academic_records FROM faculty_academic;

-- 5. Department-wise faculty count aggregation
SELECT department, COUNT(*) AS faculty_count
FROM faculty
GROUP BY department;

-- 6. Relational JOIN Query (Combining both tables)
SELECT
    f.faculty_id,
    f.faculty_name,
    f.department,
    f.designation,
    a.ug_qualification,
    a.pg_qualification,
    a.phd_qualification,
    a.research_interest,
    a.publication_count
FROM faculty f
JOIN faculty_academic a
ON f.faculty_id = a.faculty_id;
"""

with open("database/verification.sql", "w", encoding="utf-8") as f:
    f.write(verification_sql)

print("SQL Files Generated Successfully:")
print("- database/schema.sql")
print("- database/seed.sql")
print("- database/verification.sql")
