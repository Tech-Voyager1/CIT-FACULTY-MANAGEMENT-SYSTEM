-- ============================================================
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
    experience_years INT DEFAULT NULL,
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
