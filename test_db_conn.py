import mysql.connector

user_name = "adimp"
passwords = [
    "", "root", "admin", "password", "123456", "1234", "12345678",
    "root1234", "adimp", "Adimp", "adimp123", "Adimp123", "adimp@123", "Adimp@123",
    "cit", "CIT", "cit123", "cit2026", "dbms", "dbms123", "mysql123", "admin123"
]

for pwd in passwords:
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=pwd,
            port=3306
        )
        print(f"SUCCESS: Root connected with password: '{pwd}'")
        conn.close()
        break
    except mysql.connector.Error as err:
        pass
