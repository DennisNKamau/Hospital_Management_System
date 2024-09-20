# lib/models/patient.py
from models.__init__ import CONN, CURSOR
from models.medical_record import MedicalRecord
from models.appointment import Appointment

class Patient:
    
    all = {}
    
    def __init__(self, first_name, last_name, age, gender, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.medical_records = []
        self.appointments = []

    def __repr__(self):
        return (
            f"Patient(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, age={self.age}, gender={self.gender}, medical_records={self.medical_records}, appointments={self.appointments})"
        )
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str) and len(first_name) > 0:
            self._first_name = first_name
        else:
            raise ValueError("First name must be a non-empty string")

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str) and len(last_name) > 0:
            self._last_name = last_name
        else:
            raise ValueError("Last name must be a non-empty string")
            
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, age):
        if isinstance(age, int) and age > 0:
            self._age = age
        else:
            raise ValueError("Age must be a positive integer")
    
    @property
    def gender(self):
        return self._gender
    
    @gender.setter
    def gender(self, gender):
        if isinstance(gender, str) and gender in ["Male", "Female", "Other"]:
            self._gender = gender
        else:
            raise ValueError("Gender must be 'Male', 'Female', or 'Other'")
    
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Patient instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """Drop the table that persists the attributes of Patient instances"""
        sql = "DROP TABLE IF EXISTS patients"
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """Persist the attributes of a Patient instance to the database"""
        sql = """
            INSERT INTO patients (first_name, last_name, age, gender)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.age, self.gender))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    def update(self):
        """Update the table row corresponding to the current Patient instance"""
        sql = """
            UPDATE patients
            SET first_name = ?, last_name = ?, age = ?, gender = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.age, self.gender, self.id))
        CONN.commit()
    
    def delete(self):
        """Delete the table row corresponding to the current Patient instance"""
        sql = "DELETE FROM patients WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
    
    @classmethod
    def create(cls, first_name, last_name, age, gender):
        """Create a new Patient instance and persist it to the database"""
        patient = cls(first_name, last_name, age, gender)
        patient.save()
        return patient
    
    @classmethod
    def instance_from_db(cls, row):
        """Return a Patient object having the attribute values from the table row."""
        patient = cls.all.get(row[0])
        if patient:
            patient.first_name = row[1]
            patient.last_name = row[2]
            patient.age = row[3]
            patient.gender = row[4]
        else:
            patient = cls(row[1], row[2], row[3], row[4], id=row[0])
            cls.all[row[0]] = patient
        
        # Retrieve and assign related medical records
        patient.medical_records = MedicalRecord.find_by_patient_id(patient.id)
        # Retrieve and assign related appointments
        patient.appointments = Appointment.find_by_patient_id(patient.id)
        
        return patient
    
    @classmethod
    def get_all(cls):
        """Return a list of all Patient instances persisted to the database"""
        sql = "SELECT * FROM patients"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return the Patient instance with the given primary key"""
        sql = "SELECT * FROM patients WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, first_name, last_name):
        """Return a list of Patient instances with the given name"""
        sql = "SELECT * FROM patients WHERE first_name = ? AND last_name = ?"
        row = CURSOR.execute(sql, (first_name, last_name)).fetchone()
        return cls.instance_from_db(row) if row else None
    
def manage_patients():
    while True:
        print("\n--- Patient Management Menu ---")
        print("1. View all patients")
        print("2. Add a new patient")
        print("3. Update a patient")
        print("4. Delete a patient")
        print("5. Return to main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_all_patients()
        elif choice == "2":
            add_patient()
        elif choice == "3":
            update_patient()
        elif choice == "4":
            delete_patient()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def view_all_patients():
    patients = Patient.get_all()
    if patients:
        for patient in patients:
            print(patient)
    else:
        print("No patients found.")

def add_patient():
    first_name = input("Enter patient's first name: ")
    last_name = input("Enter patient's last name: ")
    age = int(input("Enter patient's age: "))
    gender = input("Enter patient's gender (Male/Female/Other): ")
    
    try:
        patient = Patient.create(first_name, last_name, age, gender)
        print(f"Patient {patient.first_name} {patient.last_name} added successfully.")
    except ValueError as e:
        print(f"Error: {e}")

def update_patient():
    patient_id = int(input("Enter patient ID to update: "))
    patient = Patient.find_by_id(patient_id)
    
    if patient:
        new_first_name = input(f"Enter new first name (current: {patient.first_name}): ")
        new_last_name = input(f"Enter new last name (current: {patient.last_name}): ")
        new_age = int(input(f"Enter new age (current: {patient.age}): "))
        new_gender = input(f"Enter new gender (current: {patient.gender}): ")
        
        try:
            patient.first_name = new_first_name
            patient.last_name = new_last_name
            patient.age = new_age
            patient.gender = new_gender
            patient.update()
            print(f"Patient {patient.first_name} {patient.last_name} updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Patient not found.")

def delete_patient():
    patient_id = int(input("Enter patient ID to delete: "))
    patient = Patient.find_by_id(patient_id)
    
    if patient:
        confirm = input(f"Are you sure you want to delete patient {patient.first_name} {patient.last_name}? (y/n): ")
        if confirm.lower() == 'y':
            patient.delete()
            print(f"Patient {patient.first_name} {patient.last_name} deleted successfully.")
    else:
        print("Patient not found.")