# lib/cli.py
import sys
from models.patient import manage_patients
from models.doctor import manage_doctors
from models.appointment import manage_appointments
from models.medical_record import manage_medical_records

from helpers import (
    exit_program,
    helper_1
)


def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            manage_patients()
        elif choice == "2":
            manage_doctors()
        elif choice == "3":
            manage_appointments()
        elif choice == "4":
            manage_medical_records()
        elif choice == "5":
            exit_program()
        else:
            print("Invalid choice. Please try again.")



def menu():
    print("\n--- Hospital Management System ---")
    print("1. Manage Patients")
    print("2. Manage Doctors")
    print("3. Manage Appointments")
    print("4. Manage Medical Records")
    print("5. Exit")

        




if __name__ == "__main__":
    main()