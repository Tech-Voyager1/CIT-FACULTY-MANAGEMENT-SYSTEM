import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_config():
    """Reads database configuration from environment variables."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "cit_faculty_db")
    }

def get_connection(include_db=True):
    """Establishes a connection to the MySQL database."""
    config = get_db_config()
    if not include_db:
        config_copy = config.copy()
        config_copy.pop("database", None)
        return mysql.connector.connect(**config_copy)
    return mysql.connector.connect(**config)

def setup_database_schema():
    """Initializes the database schema and seed data if missing."""
    try:
        # 1. Connect without DB selected to ensure Database exists
        conn = get_connection(include_db=False)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cit_faculty_db;")
        cursor.close()
        conn.close()

        # 2. Connect to cit_faculty_db and check tables
        conn = get_connection(include_db=True)
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES LIKE 'faculty';")
        faculty_exists = cursor.fetchone()

        cursor.execute("SHOW TABLES LIKE 'faculty_academic';")
        academic_exists = cursor.fetchone()

        if not faculty_exists or not academic_exists:
            # Execute schema.sql
            schema_path = os.path.join("database", "schema.sql")
            if os.path.exists(schema_path):
                with open(schema_path, "r", encoding="utf-8") as f:
                    schema_sql = f.read()
                for stmt in schema_sql.split(";"):
                    stmt = stmt.strip()
                    if stmt:
                        cursor.execute(stmt)

            # Execute seed.sql
            seed_path = os.path.join("database", "seed.sql")
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding="utf-8") as f:
                    seed_sql = f.read()
                for stmt in seed_sql.split(";"):
                    stmt = stmt.strip()
                    if stmt:
                        cursor.execute(stmt)

            conn.commit()

        cursor.close()
        conn.close()
        return True, "Database initialized successfully."
    except mysql.connector.Error as err:
        return False, f"MySQL Error during initialization: {err.msg}"
    except Exception as e:
        return False, f"Unexpected error during DB setup: {str(e)}"

def get_dashboard_counts():
    """Fetches faculty counts overall and per department."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM faculty;")
        total_row = cursor.fetchone()
        total = total_row["total"] if total_row else 0

        cursor.execute("""
            SELECT department, COUNT(*) AS count 
            FROM faculty 
            GROUP BY department;
        """)
        rows = cursor.fetchall()

        counts = {
            "Total": total,
            "CSE": 0,
            "ECE": 0,
            "EEE": 0,
            "MECH": 0,
            "CIVIL": 0
        }

        dept_map = {
            "Computer Science and Engineering": "CSE",
            "Electronics and Communication Engineering": "ECE",
            "Electrical and Electronics Engineering": "EEE",
            "Mechanical Engineering": "MECH",
            "Civil Engineering": "CIVIL"
        }

        for r in rows:
            dept_name = r["department"]
            abbr = dept_map.get(dept_name)
            if abbr:
                counts[abbr] = r["count"]

        cursor.close()
        conn.close()
        return counts
    except Exception as e:
        print("Error fetching dashboard counts:", e)
        return {"Total": 0, "CSE": 0, "ECE": 0, "EEE": 0, "MECH": 0, "CIVIL": 0}

def get_faculty_list(search_field="All Fields", search_text="", department_filter="All"):
    """Fetches records from 'faculty' table based on search parameters."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT faculty_id, faculty_name, department, designation, email, phone, joining_date FROM faculty WHERE 1=1"
        params = []

        if department_filter and department_filter != "All":
            sql += " AND department = %s"
            params.append(department_filter)

        if search_text and search_text.strip():
            query_str = f"%{search_text.strip()}%"
            if search_field == "Faculty Name":
                sql += " AND faculty_name LIKE %s"
                params.append(query_str)
            elif search_field == "Department":
                sql += " AND department LIKE %s"
                params.append(query_str)
            elif search_field == "Designation":
                sql += " AND designation LIKE %s"
                params.append(query_str)
            elif search_field == "Faculty ID":
                sql += " AND faculty_id LIKE %s"
                params.append(query_str)
            else:
                sql += " AND (faculty_id LIKE %s OR faculty_name LIKE %s OR department LIKE %s OR designation LIKE %s OR email LIKE %s)"
                params.extend([query_str, query_str, query_str, query_str, query_str])

        sql += " ORDER BY faculty_id ASC;"
        cursor.execute(sql, tuple(params))
        records = cursor.fetchall()

        cursor.close()
        conn.close()
        return records
    except Exception as e:
        print("Error fetching faculty list:", e)
        return []

def get_academic_list(search_field="All Fields", search_text=""):
    """Fetches records from 'faculty_academic' table based on search parameters."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT academic_id, faculty_id, ug_qualification, pg_qualification, phd_qualification, research_interest, publication_count FROM faculty_academic WHERE 1=1"
        params = []

        if search_text and search_text.strip():
            query_str = f"%{search_text.strip()}%"
            if search_field == "Academic ID":
                sql += " AND academic_id LIKE %s"
                params.append(query_str)
            elif search_field == "Faculty ID":
                sql += " AND faculty_id LIKE %s"
                params.append(query_str)
            elif search_field == "UG Qualification":
                sql += " AND ug_qualification LIKE %s"
                params.append(query_str)
            elif search_field == "PG Qualification":
                sql += " AND pg_qualification LIKE %s"
                params.append(query_str)
            elif search_field == "Ph.D. Qualification":
                sql += " AND phd_qualification LIKE %s"
                params.append(query_str)
            elif search_field == "Research Interest":
                sql += " AND research_interest LIKE %s"
                params.append(query_str)
            else:
                sql += " AND (academic_id LIKE %s OR faculty_id LIKE %s OR ug_qualification LIKE %s OR pg_qualification LIKE %s OR phd_qualification LIKE %s OR research_interest LIKE %s)"
                params.extend([query_str, query_str, query_str, query_str, query_str, query_str])

        sql += " ORDER BY academic_id ASC;"
        cursor.execute(sql, tuple(params))
        records = cursor.fetchall()

        cursor.close()
        conn.close()
        return records
    except Exception as e:
        print("Error fetching academic list:", e)
        return []

def get_all_faculty_ids():
    """Returns a list of all existing faculty_ids from the faculty table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT faculty_id FROM faculty ORDER BY faculty_id ASC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [r[0] for r in rows]
    except Exception as e:
        print("Error fetching faculty IDs:", e)
        return []

def get_full_faculty_profile(faculty_id):
    """Executes a relational JOIN query to retrieve complete faculty & academic details."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                f.faculty_id,
                f.faculty_name,
                f.department,
                f.designation,
                f.email,
                f.phone,
                f.joining_date,
                a.academic_id,
                a.ug_qualification,
                a.pg_qualification,
                a.phd_qualification,
                a.research_interest,
                a.publication_count
            FROM faculty f
            LEFT JOIN faculty_academic a ON f.faculty_id = a.faculty_id
            WHERE f.faculty_id = %s;
        """
        cursor.execute(sql, (faculty_id,))
        profile = cursor.fetchone()

        cursor.close()
        conn.close()
        return profile
    except Exception as e:
        print("Error fetching full profile:", e)
        return None

def get_single_faculty_record(faculty_id):
    """Fetches a single row from faculty table."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM faculty WHERE faculty_id = %s;", (faculty_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        print("Error fetching single faculty record:", e)
        return None

def get_single_academic_record(academic_id):
    """Fetches a single row from faculty_academic table."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM faculty_academic WHERE academic_id = %s;", (academic_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        print("Error fetching single academic record:", e)
        return None

def generate_next_faculty_id(department):
    """Generates next logical Faculty ID (e.g. CSE007)."""
    prefix_map = {
        "Computer Science and Engineering": "CSE",
        "Electronics and Communication Engineering": "ECE",
        "Electrical and Electronics Engineering": "EEE",
        "Mechanical Engineering": "MECH",
        "Civil Engineering": "CIVIL"
    }
    prefix = prefix_map.get(department, "FAC")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_id LIKE %s ORDER BY faculty_id DESC LIMIT 1;", (f"{prefix}%",))
        last_fac = cursor.fetchone()
        next_num = 1
        if last_fac and last_fac[0]:
            try:
                num_part = int(last_fac[0].replace(prefix, ""))
                next_num = num_part + 1
            except ValueError:
                next_num = 1
        cursor.close()
        conn.close()
        return f"{prefix}{next_num:03d}"
    except Exception:
        return f"{prefix}001"

def generate_next_academic_id():
    """Generates next logical Academic ID (e.g. ACA031)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT academic_id FROM faculty_academic ORDER BY academic_id DESC LIMIT 1;")
        last_aca = cursor.fetchone()
        next_num = 1
        if last_aca and last_aca[0]:
            try:
                num_part = int(last_aca[0].replace("ACA", ""))
                next_num = num_part + 1
            except ValueError:
                next_num = 1
        cursor.close()
        conn.close()
        return f"ACA{next_num:03d}"
    except Exception:
        return "ACA001"

# --- TABLE 1: FACULTY CRUD OPERATIONS ---
def add_single_faculty(fac_data):
    """Inserts a record directly into the faculty table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO faculty (faculty_id, faculty_name, department, designation, email, phone, joining_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            fac_data["faculty_id"],
            fac_data["faculty_name"],
            fac_data["department"],
            fac_data["designation"],
            fac_data["email"] if fac_data["email"] else None,
            fac_data["phone"] if fac_data["phone"] else None,
            fac_data["joining_date"] if fac_data["joining_date"] else None
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Faculty record '{fac_data['faculty_id']}' added successfully."
    except mysql.connector.Error as err:
        return False, f"MySQL Error: {err.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def update_single_faculty(fac_data):
    """Updates a record in the faculty table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE faculty 
            SET faculty_name = %s, department = %s, designation = %s, email = %s, phone = %s, joining_date = %s
            WHERE faculty_id = %s;
        """
        values = (
            fac_data["faculty_name"],
            fac_data["department"],
            fac_data["designation"],
            fac_data["email"] if fac_data["email"] else None,
            fac_data["phone"] if fac_data["phone"] else None,
            fac_data["joining_date"] if fac_data["joining_date"] else None,
            fac_data["faculty_id"]
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Faculty record '{fac_data['faculty_id']}' updated successfully."
    except mysql.connector.Error as err:
        return False, f"MySQL Error: {err.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def delete_single_faculty(faculty_id):
    """Deletes a record from the faculty table (CASCADE deletes associated academic record)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM faculty WHERE faculty_id = %s;"
        cursor.execute(sql, (faculty_id,))
        conn.commit()

        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected > 0:
            return True, f"Faculty record '{faculty_id}' deleted successfully."
        else:
            return False, f"Record '{faculty_id}' not found."
    except mysql.connector.Error as err:
        return False, f"MySQL Error: {err.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

# --- TABLE 2: FACULTY ACADEMIC CRUD OPERATIONS ---
def add_single_academic(aca_data):
    """Inserts a record into faculty_academic table after foreign key verification."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # FK Verification: Check if faculty_id exists in faculty table
        cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_id = %s;", (aca_data["faculty_id"],))
        parent_row = cursor.fetchone()
        if not parent_row:
            cursor.close()
            conn.close()
            return False, f"Foreign Key Error: Faculty ID '{aca_data['faculty_id']}' does not exist in the faculty table. Please select an existing Faculty ID."

        sql = """
            INSERT INTO faculty_academic (academic_id, faculty_id, ug_qualification, pg_qualification, phd_qualification, research_interest, publication_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        pub_cnt = int(aca_data["publication_count"]) if aca_data["publication_count"] and str(aca_data["publication_count"]).isdigit() else None
        values = (
            aca_data["academic_id"],
            aca_data["faculty_id"],
            aca_data["ug_qualification"] if aca_data["ug_qualification"] else None,
            aca_data["pg_qualification"] if aca_data["pg_qualification"] else None,
            aca_data["phd_qualification"] if aca_data["phd_qualification"] else None,
            aca_data["research_interest"] if aca_data["research_interest"] else None,
            pub_cnt
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Faculty Academic record '{aca_data['academic_id']}' added successfully."
    except mysql.connector.Error as err:
        return False, f"MySQL Error: {err.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def update_single_academic(aca_data):
    """Updates a record in faculty_academic table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE faculty_academic
            SET ug_qualification = %s, pg_qualification = %s, phd_qualification = %s, research_interest = %s, publication_count = %s
            WHERE academic_id = %s;
        """
        pub_cnt = int(aca_data["publication_count"]) if aca_data["publication_count"] and str(aca_data["publication_count"]).isdigit() else None
        values = (
            aca_data["ug_qualification"] if aca_data["ug_qualification"] else None,
            aca_data["pg_qualification"] if aca_data["pg_qualification"] else None,
            aca_data["phd_qualification"] if aca_data["phd_qualification"] else None,
            aca_data["research_interest"] if aca_data["research_interest"] else None,
            pub_cnt,
            aca_data["academic_id"]
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Academic record '{aca_data['academic_id']}' updated successfully."
    except mysql.connector.Error as err:
        return False, f"MySQL Error: {err.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def delete_single_academic(academic_id):
    """Deletes a record from faculty_academic table using academic_id."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM faculty_academic WHERE academic_id = %s;"
        cursor.execute(sql, (academic_id,))
        conn.commit()

        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected > 0:
            return True, f"Academic record '{academic_id}' deleted successfully."
        else:
            return False, f"Academic record '{academic_id}' not found."
    except mysql.connector.Error as err:
        return False, f"MySQL Error: {err.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"
