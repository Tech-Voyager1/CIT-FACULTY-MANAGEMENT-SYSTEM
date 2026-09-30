-- ============================================================
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
