"""
One-shot patch:
 1. Remove joining_date from seed.sql (column header + all 30 value tuples)
 2. Populate NULL phones with demo numbers (sequential 9000000001..30)
 3. Apply ALTER TABLE to live DB
 4. Update schema.sql
"""
import mysql.connector, os, re
from dotenv import load_dotenv
load_dotenv()

# ── Phone assignment map (faculty_id -> demo number) ─────────────
PHONE_MAP = {
    'CSE001': '9000000001', 'CSE002': '9000000002', 'CSE003': '9000000003',
    'CSE004': '9000000004', 'CSE005': '9000000005', 'CSE006': '9000000006',
    'ECE001': '0422-2574071', 'ECE002': '0422-2574072',  # keep real ones
    'ECE003': '9000000009', 'ECE004': '9000000010',
    'ECE005': '9000000011', 'ECE006': '9000000012',
    'EEE001': '0422-2574073',  # keep real
    'EEE002': '9000000014', 'EEE003': '9000000015',
    'EEE004': '9000000016', 'EEE005': '9000000017', 'EEE006': '9000000018',
    'MECH001': '0422-2574074',  # keep real
    'MECH002': '9000000020', 'MECH003': '9000000021',
    'MECH004': '9000000022', 'MECH005': '9000000023', 'MECH006': '9000000024',
    'CIVIL001': '0422-2574075',  # keep real
    'CIVIL002': '9000000026', 'CIVIL003': '9000000027',
    'CIVIL004': '9000000028', 'CIVIL005': '9000000029', 'CIVIL006': '9585579885',  # keep real
}

# ── 1. UPDATE seed.sql ─────────────────────────────────────────────
with open('database/seed.sql', 'r', encoding='utf-8') as f:
    seed = f.read()

# Update column header
seed = seed.replace(
    'INSERT INTO faculty (faculty_id, faculty_name, department, designation, email, phone, joining_date, experience_years) VALUES',
    'INSERT INTO faculty (faculty_id, faculty_name, department, designation, email, phone, experience_years) VALUES'
)

# For each faculty row: remove joining_date (always NULL, 6th position after phone)
# Pattern: ('ID', 'name', 'dept', 'desig', 'email', PHONE, NULL, exp)
#           ^^^  need to remove the NULL before exp
def fix_row(m):
    fac_id = m.group(1)
    rest = m.group(0)
    # Replace NULL phone with real phone if needed
    phone_val = PHONE_MAP.get(fac_id, '')
    # Row format: ('ID', 'name', 'dept', 'desig', 'email', PHONE_OR_NULL, NULL_DATE, EXP)
    # Remove the NULL_DATE field (7th position)
    # Use regex to strip the 7th comma-separated value
    inner = rest[1:-2]  # strip leading ( and trailing ), or );
    trailing = rest[-2:]
    parts = [p.strip() for p in inner.split(',')]
    # parts[0]=id, [1]=name, [2]=dept, [3]=desig, [4]=email, [5]=phone, [6]=joining_date, [7]=exp
    if len(parts) >= 8:
        # Fix phone if NULL
        if parts[5] == 'NULL' and fac_id in PHONE_MAP:
            parts[5] = f"'{PHONE_MAP[fac_id]}'"
        parts = parts[:6] + parts[7:]  # remove index 6 (joining_date)
        return '(' + ', '.join(parts) + trailing
    return rest

seed = re.sub(r"\('(CSE\d+|ECE\d+|EEE\d+|MECH\d+|CIVIL\d+)', [^\n]+\n?", fix_row, seed)

with open('database/seed.sql', 'w', encoding='utf-8') as f:
    f.write(seed)
print("seed.sql updated")

# ── 2. UPDATE schema.sql ──────────────────────────────────────────
with open('database/schema.sql', 'r', encoding='utf-8') as f:
    schema = f.read()

schema = schema.replace('    joining_date DATE DEFAULT NULL,\n', '')

with open('database/schema.sql', 'w', encoding='utf-8') as f:
    f.write(schema)
print("schema.sql updated")

# ── 3. ALTER live MySQL DB ────────────────────────────────────────
cfg = {
    "host": os.getenv("DB_HOST","localhost"),
    "port": int(os.getenv("DB_PORT",3306)),
    "user": os.getenv("DB_USER","root"),
    "password": os.getenv("DB_PASSWORD",""),
    "database": os.getenv("DB_NAME","cit_faculty_db"),
}
conn = mysql.connector.connect(**cfg)
cur = conn.cursor()

# Check if joining_date still exists
cur.execute("SHOW COLUMNS FROM faculty LIKE 'joining_date';")
if cur.fetchone():
    cur.execute("ALTER TABLE faculty DROP COLUMN joining_date;")
    print("ALTER TABLE: joining_date dropped")
else:
    print("joining_date already absent from DB")

# Populate phones
for fac_id, phone in PHONE_MAP.items():
    cur.execute("UPDATE faculty SET phone = %s WHERE faculty_id = %s AND (phone IS NULL OR phone = '');", (phone, fac_id))

conn.commit()

# Verify
cur.execute("SELECT faculty_id, phone FROM faculty ORDER BY faculty_id;")
rows = cur.fetchall()
null_phones = [r for r in rows if not r[1]]
print(f"Records with no phone: {null_phones}")
print(f"Total faculty rows: {len(rows)}")

cur.execute("DESCRIBE faculty;")
print("Final schema:", [r[0] for r in cur.fetchall()])

cur.close()
conn.close()
print("DB done.")
