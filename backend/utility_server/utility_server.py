from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# SQLite database configuration
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

create_tables()

# Routes
@app.route("/", methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the utility server!'})

@app.route('/medical_records', methods=['GET'])
def get_medical_records():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_records")
    records = cursor.fetchall()
    conn.close()
    return jsonify({'medicalRecords': records})

@app.route('/medical_records', methods=['POST'])
def create_medical_record():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO medical_records VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        data['patient_id'],
        data['DrName'],
        data['approved'],
        data['declineMsg'],
        data['diagnoseDate'],
        data['dischargeDate'],
        data['disease'],
        data['hospitalRecordID'],
        data['medication'],
        str(data['reports']),
        data['treatment']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Medical record created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
