# Hospital Management System

## Overview

The Hospital Management System is designed to facilitate the management of hospital records through a simple CLI. Users can manage patients, doctors, appointments, and medical records with ease. This README provides detailed information on the project's structure and how to use it. It uses SQLite as its database to store and retrieve data efficiently.

# File Descriptions

## CLI Script

### lib/cli.py
The main entry point of the application. It displays a menu and handles user inputs to navigate through different management functions such as managing patients, doctors, appointments, and medical records.

## Models

### lib/models/patient.py
Manages patient-related operations such as adding, viewing, updating, and deleting patients.
#### Functions:
##### manage_patients(): Displays a menu for patient management and handles user input.
##### add_patient(): Adds a new patient to the database.
##### view_patients(): Lists all patients.
##### update_patient(): Updates an existing patient's information.
##### delete_patient(): Deletes a patient from the database.

### lib/models/doctor.py
Manages doctor-related operations similar to patient operations.

#### Functions

##### manage_appointments(): Displays a menu for appointment management and handles user input.
##### add_appointment(): Schedules a new appointment.
##### view_appointments(): Lists all appointments.
##### update_appointment(): Updates an existing appointment.
##### delete_appointment(): Cancels an appointment.

### lib/models/medical_record.py
Manages medical record-related operations such as adding, viewing, updating, and deleting medical records.

#### Functions
##### manage_medical_records(): Displays a menu for medical record management and handles user input.
##### add_medical_record(): Adds a new medical record to the database.
##### view_medical_records(): Lists all medical records.
##### update_medical_record(): Updates an existing medical record.
##### delete_medical_record(): Deletes a medical record from the database.


## Database Schema

### Patients Table (`patients`)
- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `name`: TEXT, NOT NULL
- `age`: INTEGER
- `gender`: TEXT
- `medical_history`: TEXT

### Doctors Table (`doctors`)
- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `name`: TEXT, NOT NULL
- `specialization`: TEXT
- `availability`: TEXT

### Appointments Table (`appointments`)
- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `patient_id`: INTEGER, FOREIGN KEY REFERENCES `patients`(`id`)
- `doctor_id`: INTEGER, FOREIGN KEY REFERENCES `doctors`(`id`)
- `appointment_date`: TEXT

### Medical Records Table (`medical_records`)
- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `patient_id`: INTEGER, FOREIGN KEY REFERENCES `patients`(`id`)
- `doctor_id`: INTEGER, FOREIGN KEY REFERENCES `doctors`(`id`)
- `record_date`: TEXT
- `diagnosis`: TEXT
- `treatment`: TEXT

## Installation

1. **Clone the repository**:
    

2. **Create a virtual environment** 
   

3. **Install dependencies**:
   

4. **Initialize the database**:
    The database will be automatically initialized when you run the main application.

## Usage

Run the application:

python3 cli.py