#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.patient import Patient

def seed_database():
    # Drop and create the patients table
    Patient.drop_table()
    Patient.create_table()

    # Create seed data for patients
    Patient.create("John", "Doe", 30, "Male")
    Patient.create("Jane", "Smith", 25, "Female")
    Patient.create("Alice", "Johnson", 40, "Female")
    Patient.create("Bob", "Brown", 50, "Male")
    Patient.create("Eve", "Davis", 35, "Female")
    Patient.create("Frank", "Wilson", 45, "Male")
    Patient.create("Grace", "Lee", 28, "Female")
    Patient.create("Hank", "Martinez", 60, "Male")
    Patient.create("Ivy", "Robinson", 32, "Female")
    Patient.create("Jack", "Clark", 38, "Male")

seed_database()
print("Seeded database")
