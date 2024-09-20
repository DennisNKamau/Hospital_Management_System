# lib/models/appointment.py
from models.__init__ import CONN, CURSOR

class Appointment:
    
    all = {}
    
    def __init__(self, appointment_date, patient_id, doctor_id, notes=None, id=None):
        self.id = id
        self.appointment_date = appointment_date
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.notes = notes

    def __repr__(self):
        return (
            f"Appointment(id={self.id}, appointment_date={self.appointment_date}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, notes={self.notes})"
        )
    
    @property
    def appointment_date(self):
        return self._appointment_date
    
    @appointment_date.setter
    def appointment_date(self, appointment_date):
        # Add validation if necessary
        self._appointment_date = appointment_date

    @property
    def patient_id(self):
        return self._patient_id
    
    @patient_id.setter
    def patient_id(self, patient_id):
        if isinstance(patient_id, int) and patient_id > 0:
            self._patient_id = patient_id
        else:
            raise ValueError("Patient ID must be a positive integer")

    @property
    def doctor_id(self):
        return self._doctor_id
    
    @doctor_id.setter
    def doctor_id(self, doctor_id):
        if isinstance(doctor_id, int) and doctor_id > 0:
            self._doctor_id = doctor_id
        else:
            raise ValueError("Doctor ID must be a positive integer")

    @property
    def notes(self):
        return self._notes
    
    @notes.setter
    def notes(self, notes):
        if notes is None or isinstance(notes, str):
            self._notes = notes
        else:
            raise ValueError("Notes must be a string or None")
    
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Appointment instances"""
        sql = """
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
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """Drop the table that persists the attributes of Appointment instances"""
        sql = "DROP TABLE IF EXISTS appointments"
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """Persist the attributes of an Appointment instance to the database"""
        sql = """
            INSERT INTO appointments (appointment_date, patient_id, doctor_id, notes)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.appointment_date, self.patient_id, self.doctor_id, self.notes))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    def update(self):
        """Update the table row corresponding to the current Appointment instance"""
        sql = """
            UPDATE appointments
            SET appointment_date = ?, patient_id = ?, doctor_id = ?, notes = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.appointment_date, self.patient_id, self.doctor_id, self.notes, self.id))
        CONN.commit()
    
    def delete(self):
        """Delete the table row corresponding to the current Appointment instance"""
        sql = "DELETE FROM appointments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
    
    @classmethod
    def create(cls, appointment_date, patient_id, doctor_id, notes=None):
        """Create a new Appointment instance and persist it to the database"""
        appointment = cls(appointment_date, patient_id, doctor_id, notes)
        appointment.save()
        return appointment
    
    @classmethod
    def instance_from_db(cls, row):
        """Return an Appointment object having the attribute values from the table row."""
        
        # Check the dictionary for existing instances using the row's primary key
        appointment = cls.all.get(row[0])
        if appointment:
            # Ensure attributes match row values in case local instance was modified
            appointment.appointment_date = row[1]
            appointment.patient_id = row[2]
            appointment.doctor_id = row[3]
            appointment.notes = row[4]
        else:
            # Create a new instance using row values
            appointment = cls(row[1], row[2], row[3], row[4], id=row[0])
            cls.all[row[0]] = appointment
        
        return appointment
    
    @classmethod
    def get_all(cls):
        """Return a list of all Appointment instances persisted to the database"""
        sql = "SELECT * FROM appointments"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return the Appointment instance with the given primary key"""
        sql = "SELECT * FROM appointments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_patient_id(cls, patient_id):
        """Return a list of Appointment instances for the given patient_id"""
        sql = "SELECT * FROM appointments WHERE patient_id = ?"
        CURSOR.execute(sql, (patient_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_doctor_id(cls, doctor_id):
        """Return a list of Appointment instances for the given doctor_id"""
        sql = "SELECT * FROM appointments WHERE doctor_id = ?"
        CURSOR.execute(sql, (doctor_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    #CLI Interface
def manage_appointments():
     while True:
        print("\n--- Manage Appointments ---")
        print("1. Create Appointment")
        print("2. View All Appointments")
        print("3. Find Appointment by ID")
        print("4. Delete Appointment")
        print("0. Back to Main Menu")
        
        choice = input("> ")
        
        if choice == "1":
            create_appointment()
        elif choice == "2":
            view_all_appointments()
        elif choice == "3":
            find_appointment_by_id()
        elif choice == "4":
            delete_appointment()
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

def create_appointment():
    try:
        appointment_date = input("Enter appointment date (YYYY-MM-DD HH:MM): ")
        patient_id = int(input("Enter patient ID: "))
        doctor_id = int(input("Enter doctor ID: "))
        notes = input("Enter notes (optional): ")
        Appointment.create(appointment_date, patient_id, doctor_id, notes)
        print("Appointment created successfully!")
    except Exception as e:
        print(f"Error creating appointment: {e}")

def view_all_appointments():
    appointments = Appointment.get_all()
    for appointment in appointments:
        print(appointment)

def find_appointment_by_id():
    try:
        appointment_id = int(input("Enter appointment ID: "))
        appointment = Appointment.find_by_id(appointment_id)
        if appointment:
            print(appointment)
        else:
            print("Appointment not found.")
    except ValueError:
        print("Invalid ID format.")

def delete_appointment():
    try:
        appointment_id = int(input("Enter appointment ID: "))
        appointment = Appointment.find_by_id(appointment_id)
        if appointment:
            appointment.delete()
            print("Appointment deleted successfully.")
        else:
            print("Appointment not found.")
    except ValueError:
        print("Invalid ID format.")
