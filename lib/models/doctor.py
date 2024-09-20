# lib/models/doctor.py
from models.__init__ import CURSOR, CONN
from models.medical_record import MedicalRecord
from models.appointment import Appointment

class Doctor:
    
    all = {}
    
    def __init__(self, name, specialization, id=None):
        self.id = id
        self.name = name
        self.specialization = specialization
        self.appointments = []
        self.medical_records = []

    def __repr__(self):
        return (
            f"Doctor(id={self.id}, name={self.name}, specialization={self.specialization}, appointments={self.appointments}, medical_records={self.medical_records})"
        )
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def specialization(self):
        return self._specialization
    
    @specialization.setter
    def specialization(self, specialization):
        if isinstance(specialization, str) and len(specialization) > 0:
            self._specialization = specialization
        else:
            raise ValueError("Specialization must be a non-empty string")
            
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Doctor instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """Drop the table that persists the attributes of Doctor instances"""
        sql = "DROP TABLE IF EXISTS doctors"
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """Persist the attributes of a Doctor instance to the database"""
        sql = """
            INSERT INTO doctors (name, specialization)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.specialization))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    def update(self):
        """Update the table row corresponding to the current Doctor instance"""
        sql = """
            UPDATE doctors
            SET name = ?, specialization = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.specialization, self.id))
        CONN.commit()
    
    def delete(self):
        """Delete the table row corresponding to the current Doctor instance"""
        sql = "DELETE FROM doctors WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
    
    @classmethod
    def create(cls, name, specialization):
        """Create a new Doctor instance and persist it to the database"""
        doctor = cls(name, specialization)
        doctor.save()
        return doctor
    
    @classmethod
    def instance_from_db(cls, row):
        """Return a Doctor object having the attribute values from the table row."""
        
        doctor = cls.all.get(row[0])
        if doctor:
            doctor.name = row[1]
            doctor.specialization = row[2]
        else:
            doctor = cls(row[1], row[2], id=row[0])
            cls.all[row[0]] = doctor
    
        doctor.appointments = Appointment.find_by_doctor_id(doctor.id)
        doctor.medical_records = MedicalRecord.find_by_doctor_id(doctor.id)
        
        return doctor
    
    @classmethod
    def get_all(cls):
        """Return a list of all Doctor instances persisted to the database"""
        sql = "SELECT * FROM doctors"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return the Doctor instance with the given primary key"""
        sql = "SELECT * FROM doctors WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """Return a list of Doctor instances with the given name"""
        sql = "SELECT * FROM doctors WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

def manage_doctors():
    """Function to manage doctor-related operations from the CLI"""
    while True:
        print("\n--- Manage Doctors ---")
        print("1. Add Doctor")
        print("2. View Doctors")
        print("3. Update Doctor")
        print("4. Delete Doctor")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter doctor's name: ")
            specialization = input("Enter doctor's specialization: ")
            Doctor.create(name, specialization)
            print(f"Doctor {name} added successfully.")
        elif choice == '2':
            doctors = Doctor.get_all()
            for doctor in doctors:
                print(doctor)
        elif choice == '3':
            id = int(input("Enter doctor's ID to update: "))
            doctor = Doctor.find_by_id(id)
            if doctor:
                doctor.name = input(f"Enter new name (current: {doctor.name}): ") or doctor.name
                doctor.specialization = input(f"Enter new specialization (current: {doctor.specialization}): ") or doctor.specialization
                doctor.update()
                print(f"Doctor {doctor.name} updated successfully.")
            else:
                print("Doctor not found.")
        elif choice == '4':
            id = int(input("Enter doctor's ID to delete: "))
            doctor = Doctor.find_by_id(id)
            if doctor:
                doctor.delete()
                print(f"Doctor {doctor.name} deleted successfully.")
            else:
                print("Doctor not found.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
