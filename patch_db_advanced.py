import os
import re

def main():
    db_file = r"d:\Downloads\DBMS Lab Project\CIT Faculty Management System\db.py"
    with open(db_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Update setup_database_schema
    setup_patch = """
        cursor.execute("SHOW TABLES LIKE 'faculty_academic';")
        academic_exists = cursor.fetchone()

        if faculty_exists:
            cursor.execute("SHOW COLUMNS FROM faculty LIKE 'experience_years';")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE faculty ADD COLUMN experience_years INT;")
                cursor.execute("UPDATE faculty SET experience_years = 11 WHERE designation LIKE 'Assistant Professor%';")
                cursor.execute("UPDATE faculty SET experience_years = 15 WHERE designation = 'Associate Professor';")
                cursor.execute("UPDATE faculty SET experience_years = 18 WHERE designation = 'Professor';")
                cursor.execute("UPDATE faculty SET experience_years = 20 WHERE designation IN ('Professor & Head', 'Principal & Professor');")
                cursor.execute("UPDATE faculty SET phone = NULL WHERE phone = '' OR phone = 'None' OR phone = 'Not Publicly Listed';")
                conn.commit()
"""
    content = content.replace(
        "cursor.execute(\"SHOW TABLES LIKE 'faculty_academic';\")\n        academic_exists = cursor.fetchone()",
        setup_patch
    )

    # 2. Update get_faculty_list
    content = content.replace(
        "SELECT faculty_id, faculty_name, department, designation, email, phone, joining_date FROM faculty",
        "SELECT faculty_id, faculty_name, department, designation, email, phone, joining_date, experience_years FROM faculty"
    )

    # 3. Update get_full_faculty_profile
    content = content.replace(
        "f.joining_date,",
        "f.joining_date,\n                f.experience_years,"
    )

    # 4. Update add_single_faculty
    content = content.replace(
        "INSERT INTO faculty (faculty_id, faculty_name, department, designation, email, phone, joining_date)",
        "INSERT INTO faculty (faculty_id, faculty_name, department, designation, email, phone, joining_date, experience_years)"
    ).replace(
        "VALUES (%s, %s, %s, %s, %s, %s, %s);",
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    )
    content = content.replace(
        "fac_data[\"joining_date\"] if fac_data[\"joining_date\"] else None",
        "fac_data[\"joining_date\"] if fac_data[\"joining_date\"] else None,\n            fac_data.get(\"experience_years\")"
    )

    # 5. Update update_single_faculty
    content = content.replace(
        "SET faculty_name = %s, department = %s, designation = %s, email = %s, phone = %s, joining_date = %s",
        "SET faculty_name = %s, department = %s, designation = %s, email = %s, phone = %s, joining_date = %s, experience_years = %s"
    )
    # The values tuple in update_single_faculty has faculty_id at the end.
    content = content.replace(
        "fac_data[\"joining_date\"] if fac_data[\"joining_date\"] else None,\n            fac_data[\"faculty_id\"]",
        "fac_data[\"joining_date\"] if fac_data[\"joining_date\"] else None,\n            fac_data.get(\"experience_years\"),\n            fac_data[\"faculty_id\"]"
    )

    # 6. Add execute_advanced_query
    advanced_query_code = """
def execute_advanced_query(query_type, conditions, sort_by=None, sort_order="ASC"):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Determine if JOIN is needed
        # Fields mapping
        fac_fields = ['faculty_id', 'faculty_name', 'department', 'designation', 'email', 'phone', 'joining_date', 'experience_years']
        aca_fields = ['academic_id', 'ug_qualification', 'pg_qualification', 'phd_qualification', 'research_interest', 'publication_count']
        
        needs_join = False
        for c in conditions:
            if c['field'] in aca_fields:
                needs_join = True
                
        if sort_by in aca_fields:
            needs_join = True
            
        if query_type == "Count":
            if needs_join:
                base_sql = "SELECT COUNT(*) as cnt FROM faculty f JOIN faculty_academic a ON f.faculty_id = a.faculty_id"
            else:
                base_sql = "SELECT COUNT(*) as cnt FROM faculty f"
        else:
            if needs_join:
                base_sql = \"\"\"SELECT f.faculty_id, f.faculty_name, f.department, f.designation, f.email, f.phone, f.joining_date, f.experience_years,
                                     a.academic_id, a.ug_qualification, a.pg_qualification, a.phd_qualification, a.research_interest, a.publication_count
                              FROM faculty f JOIN faculty_academic a ON f.faculty_id = a.faculty_id\"\"\"
            else:
                base_sql = "SELECT f.* FROM faculty f"

        where_clauses = []
        params = []
        
        for i, cond in enumerate(conditions):
            logic = cond['logic'] if i > 0 else ""
            field = cond['field']
            op = cond['op']
            val = cond['val']
            
            prefix = "a." if field in aca_fields else "f."
            
            if op in ('IS NULL', 'IS NOT NULL'):
                clause = f"{logic} {prefix}{field} {op}".strip()
            else:
                if op == 'LIKE':
                    val = f"%{val}%"
                clause = f"{logic} {prefix}{field} {op} %s".strip()
                params.append(val)
                
            where_clauses.append(clause)
            
        sql = base_sql
        if where_clauses:
            sql += " WHERE " + " ".join(where_clauses)
            
        if query_type != "Count" and sort_by:
            prefix = "a." if sort_by in aca_fields else "f."
            sql += f" ORDER BY {prefix}{sort_by} {sort_order}"
            
        sql += ";"
        
        cursor.execute(sql, tuple(params))
        if query_type == "Count":
            result = cursor.fetchone()
            rows_returned = 1
            ret = result['cnt']
        else:
            ret = cursor.fetchall()
            rows_returned = len(ret)
            
        import db_logger
        db_logger.notify_sql(sql, tuple(params), True, rows_returned)
        
        cursor.close()
        conn.close()
        return True, ret
    except Exception as e:
        import db_logger
        db_logger.notify_sql(locals().get('sql', ''), tuple(params), False, 0, str(e))
        return False, str(e)
"""
    if "def execute_advanced_query(" not in content:
        content += advanced_query_code
        
    with open(db_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("db.py patched successfully.")

if __name__ == "__main__":
    main()
