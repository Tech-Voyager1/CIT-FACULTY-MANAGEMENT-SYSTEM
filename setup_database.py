"""
setup_database.py
-----------------
One-shot database initializer for CIT Faculty Management System.
Run this once on a fresh machine before launching main.py.

Usage:
    python setup_database.py
"""

import os
import sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = int(os.getenv("DB_PORT", 3306))
DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME     = os.getenv("DB_NAME", "cit_faculty_db")

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = os.path.join(BASE_DIR, "database", "schema.sql")
SEED_FILE   = os.path.join(BASE_DIR, "database", "seed.sql")


def run_sql_file(cursor, filepath):
    """Executes a .sql file statement-by-statement safely."""
    if not os.path.exists(filepath):
        print(f"  [WARN] File not found: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Strip single-line comments (-- ...)
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        cleaned_lines.append(line)
        
    cleaned_sql = "".join(cleaned_lines)
    for stmt in cleaned_sql.split(";"):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)


def main():
    print("=" * 60)
    print("  CIT Faculty Management System - Database Setup")
    print("=" * 60)
    print(f"  Host     : {DB_HOST}:{DB_PORT}")
    print(f"  User     : {DB_USER}")
    print(f"  Database : {DB_NAME}")
    print()

    # -- Step 1: Connect WITHOUT database to create it if missing --
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASSWORD
        )
    except mysql.connector.Error as e:
        print(f"[ERROR] Cannot connect to MySQL: {e.msg}")
        print()
        print("  Check that:")
        print("    - MySQL server is running")
        print("    - Credentials in .env are correct")
        sys.exit(1)

    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.commit()
    print(f"[OK] Database '{DB_NAME}' ready.")

    # -- Step 2: Switch to the database ----------------------------
    cursor.execute(f"USE `{DB_NAME}`;")

    # -- Step 3: Execute schema.sql --------------------------------
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        run_sql_file(cursor, SCHEMA_FILE)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print("[OK] schema.sql executed - tables created.")
    except mysql.connector.Error as e:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print(f"[ERROR] schema.sql failed: {e.msg}")
        cursor.close(); conn.close(); sys.exit(1)

    # -- Step 4: Execute seed.sql ----------------------------------
    try:
        run_sql_file(cursor, SEED_FILE)
        conn.commit()
        print("[OK] seed.sql executed - sample data loaded.")
    except mysql.connector.Error as e:
        print(f"[WARN] seed.sql: {e.msg} (data may already exist - that's OK)")

    # ── Step 5: Verify ────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM faculty;")
    fac_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM faculty_academic;")
    aca_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    print()
    print("=" * 60)
    print(f"  faculty          : {fac_count} records")
    print(f"  faculty_academic : {aca_count} records")
    print("=" * 60)
    print()
    print("[DONE] Database setup complete. You can now run:  python main.py")
    print()


if __name__ == "__main__":
    main()
