import sqlite3
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.medical_record import MedicalRecord

DB_PATH = "hospital.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # users table: id, username, password, role (Doctor/Patient)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')
    
    # doctors table: id, user_id, name, specialty
    c.execute('''CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        specialty TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    # patients table: id, user_id, name
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    # appointments table
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER,
        patient_id INTEGER,
        time_slot TEXT,
        FOREIGN KEY(doctor_id) REFERENCES doctors(id),
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )''')
    
    # medical records table
    c.execute('''CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        record_text TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )''')
    
    conn.commit()
    conn.close()

def register_user(username, password, role, name, specialty=""):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        user_id = c.lastrowid
        if role == "Doctor":
            c.execute("INSERT INTO doctors (user_id, name, specialty) VALUES (?, ?, ?)", (user_id, name, specialty))
        elif role == "Patient":
            c.execute("INSERT INTO patients (user_id, name) VALUES (?, ?)", (user_id, name))
        conn.commit()
        return True, "Registration successful."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    if user:
        user_id, role = user
        if role == "Doctor":
            c.execute("SELECT id, name, specialty FROM doctors WHERE user_id = ?", (user_id,))
            doc = c.fetchone()
            conn.close()
            if doc:
                return True, {"role": role, "id": doc[0], "name": doc[1], "specialty": doc[2]}
        elif role == "Patient":
            c.execute("SELECT id, name FROM patients WHERE user_id = ?", (user_id,))
            pat = c.fetchone()
            conn.close()
            if pat:
                return True, {"role": role, "id": pat[0], "name": pat[1]}
    conn.close()
    return False, "Invalid credentials."

def get_all_doctors():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, specialty FROM doctors")
    rows = c.fetchall()
    conn.close()
    doctors = []
    for row in rows:
        doctors.append(Doctor(row[0], row[1], row[2]))
    return doctors

def get_all_patients():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM patients")
    rows = c.fetchall()
    patients = []
    for row in rows:
        patient = Patient(row[0], row[1])
        c.execute("SELECT record_text FROM medical_records WHERE patient_id = ?", (row[0],))
        records = c.fetchall()
        # populate history
        if records:
            patient.medical_record._MedicalRecord__history = [r[0] for r in records]
        patients.append(patient)
    conn.close()
    return patients

def get_appointments():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT a.id, a.time_slot, d.id, d.name, d.specialty, p.id, p.name 
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        JOIN patients p ON a.patient_id = p.id
    """)
    rows = c.fetchall()
    conn.close()
    appts = []
    for row in rows:
        appt_id, time_slot, d_id, d_name, d_specialty, p_id, p_name = row
        doc = Doctor(d_id, d_name, d_specialty)
        pat = Patient(p_id, p_name)
        appts.append(Appointment(doc, pat, time_slot, appt_id))
    return appts

def add_appointment(doctor_id, patient_id, time_slot):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO appointments (doctor_id, patient_id, time_slot) VALUES (?, ?, ?)", (doctor_id, patient_id, time_slot))
    conn.commit()
    conn.close()

def remove_appointment(appt_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM appointments WHERE id = ?", (appt_id,))
    conn.commit()
    conn.close()

def add_medical_record(patient_id, record):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO medical_records (patient_id, record_text) VALUES (?, ?)", (patient_id, record))
    conn.commit()
    conn.close()
