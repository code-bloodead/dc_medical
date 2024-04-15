import sqlite3

DB_FILE = 'medical_records.db'

# Create tables if they don't exist
def create_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL,
            DrName TEXT NOT NULL,
            approved BOOLEAN,
            declineMsg TEXT,
            diagnoseDate INTEGER,
            dischargeDate INTEGER,
            disease TEXT,
            hospitalRecordID TEXT,
            medication TEXT,
            reports TEXT,
            treatment TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    conn.commit()
    conn.close()


# Seed the database with some initial data
def seed_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name) VALUES ('John Doe')")
    cursor.execute("INSERT INTO patients (name) VALUES ('Jane Smith')")
    conn.commit()
    conn.close()


# Seed the medical records
def seed_medical_records():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM patients")
    patient_ids = cursor.fetchall()
    for patient_id in patient_ids:
        cursor.execute("INSERT INTO medical_records (patient_id, DrName, approved, declineMsg, diagnoseDate, dischargeDate, disease, hospitalRecordID, medication, reports, treatment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            patient_id[0],
            'Dr. John Smith',
            True,
            '',
            '1656485952',
            '0',
            'Diabetes',
            'JH01',
            'Glipizide, Dulaglutide',
            '["B080.pdf"]',
            'Controlling blood sugar through diet, oral medication'
        ))
    conn.commit()
    conn.close()


create_tables()
seed_data()
seed_medical_records()
