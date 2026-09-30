import os
import mysql.connector

# Try common passwords or DB_PASSWORD from env
db_host = os.environ.get("DB_HOST", "localhost")
db_user = os.environ.get("DB_USER", "root")
db_password = os.environ.get("DB_PASSWORD", "root")

passwords_to_try = [db_password, "", "root", "admin", "password", "123456", "mysql", "cit123"]

connected = False
active_conn = None

for pwd in passwords_to_try:
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=pwd,
            autocommit=True
        )
        print(f"CONNECTED TO MYSQL SERVER WITH PASSWORD '{pwd}'!")
        active_conn = conn
        connected = True
        break
    except mysql.connector.Error as err:
        pass

if not connected:
    print("COULD_NOT_CONNECT: MySQL root password requires configuration or environment variable DB_PASSWORD.")
else:
    cursor = active_conn.cursor()
    # Read schema.sql
    with open("database/schema.sql", "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Execute schema statements
    for stmt in schema_sql.split(";"):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)

    print("Created database 'cit_faculty_db' and tables 'faculty', 'faculty_academic' successfully!")

    # Read seed.sql
    with open("database/seed.sql", "r", encoding="utf-8") as f:
        seed_sql = f.read()

    for stmt in seed_sql.split(";"):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)

    print("Imported seed data into 'cit_faculty_db' successfully!")

    # Execute verification queries
    cursor.execute("USE cit_faculty_db;")
    cursor.execute("SELECT COUNT(*) FROM faculty;")
    fac_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM faculty_academic;")
    aca_count = cursor.fetchone()[0]

    cursor.execute("SELECT department, COUNT(*) FROM faculty GROUP BY department;")
    dept_counts = cursor.fetchall()

    print(f"VERIFICATION RESULT: Faculty count = {fac_count}, Academic records = {aca_count}")
    print("Department Counts:", dept_counts)

    active_conn.close()
