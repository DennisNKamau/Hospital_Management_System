import sqlite3

CONN = sqlite3.connect('hospital.db')
CURSOR = CONN.cursor()

def initialize_database():
    create_doctors_table_sql = """
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL
        )
    """
    CURSOR.execute(create_doctors_table_sql)

create_appointments_table_sql = """
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY,
        appointment_date TEXT NOT NULL,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    )
"""

CURSOR.execute(create_appointments_table_sql)

create_medical_records_table_sql = """
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        record_date TEXT NOT NULL,
        diagnosis TEXT NOT NULL,
        treatment TEXT NOT NULL,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    )
"""

CURSOR.execute(create_medical_records_table_sql)

create_patients_table_sql = """
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL
    )
"""

CURSOR.execute(create_patients_table_sql)



CONN.commit()

initialize_database()
