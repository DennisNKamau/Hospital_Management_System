# cli/main.py

from models.patient import Patient
from models.medical_record import MedicalRecord
from models.doctor import Doctor

def create_tables():
    Patient.create_table()
    Doctor.create_table()
    MedicalRecord.create_table()

def add_medical_record():
    patient_id = int(input("Enter patient ID: "))
    doctor_id = int(input("Enter doctor ID: "))
    record_date = input("Enter record date (YYYY-MM-DD): ")
    diagnosis = input("Enter diagnosis: ")
    treatment = input("Enter treatment: ")
    new_record = MedicalRecord.create(patient_id, doctor_id, record_date, diagnosis, treatment)
    print(f"Medical Record added with ID {new_record.id}.")

def view_medical_records():
    records = MedicalRecord.get_all()
    for record in records:
        print(f"ID: {record.id}, Patient ID: {record.patient_id}, Doctor ID: {record.doctor_id}, Record Date: {record.record_date}, Diagnosis: {record.diagnosis}, Treatment: {record.treatment}")

def update_medical_record():
    record_id = int(input("Enter medical record ID to update: "))
    record = MedicalRecord.find_by_id(record_id)
    if record:
        patient_id = int(input(f"Enter new patient ID (current: {record.patient_id}): "))
        doctor_id = int(input(f"Enter new doctor ID (current: {record.doctor_id}): "))
        record_date = input(f"Enter new record date (YYYY-MM-DD) (current: {record.record_date}): ")
        diagnosis = input(f"Enter new diagnosis (current: {record.diagnosis}): ")
        treatment = input(f"Enter new treatment (current: {record.treatment}): ")
        record.patient_id = patient_id
        record.doctor_id = doctor_id
        record.record_date = record_date
        record.diagnosis = diagnosis
        record.treatment = treatment
        record.update()
        print("Medical Record updated successfully.")
    else:
        print("Medical Record not found.")

def delete_medical_record():
    record_id = int(input("Enter medical record ID to delete: "))
    record = MedicalRecord.find_by_id(record_id)
    if record:
        record.delete()
        print("Medical Record deleted successfully.")
    else:
        print("Medical Record not found.")

def manage_medical_records():
    actions = {
        "1": add_medical_record,
        "2": view_medical_records,
        "3": update_medical_record,
        "4": delete_medical_record,
    }

    while True:
        print("""
        Medical Record Management
        1. Add Medical Record
        2. View Medical Records
        3. Update Medical Record
        4. Delete Medical Record
        5. Back to Main Menu
        """)
        choice = input("Choose an option: ")
        if choice == "5":
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please try again.")

def main():
    create_tables()

    actions = {
        "1": manage_medical_records,
        # Add other main menu actions here
    }

    while True:
        print("""
        Hospital Management System
        1. Manage Medical Records
        2. Exit
        """)
        choice = input("Choose an option: ")
        if choice == "2":
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
