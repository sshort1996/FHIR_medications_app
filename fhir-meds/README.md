# Medication Management App

The Medication Management App is a Flask-based web application that allows users to manage their medications. The app provides various features such as user registration and login, medication details view, contact details input for reminders, and administrative capabilities for prescribers.

## Features

- User Registration and Login: Users can create an account and log in to access their medication-related information.
- Medication Details: Users can view their medication details, including prescription information and dosage instructions.
- Reminders via SMS or Email: Users can provide their contact details to receive reminders for taking medications.
- Administrative Capabilities: Admin users or prescribers can log in to view, update, or delete prescriptions.
- Security Measures:
  - Password Hashing and Salting: User credentials are securely stored using hashing and salting techniques.
  - Email Authentication: User accounts are authenticated through email verification.
  - Strong Password Enforcement: Users are required to create strong passwords to ensure account security.
  - Restricted Subdomains: Certain subdomains may require authorization to access, ensuring data privacy.
  - Input Sanitization: All user inputs are properly sanitized to prevent SQL injections.

## Architecture

The Medication Management App leverages the [Fast Healthcare Interoperability Resources (FHIR)](https://www.hl7.org/fhir/) standard for storing medically relevant data. The following architecture notes should be considered:

- FHIR Server: All medically relevant data, including patient information, medications, and prescription details, are stored in a FHIR server.
- FHIR Client Library: The app utilizes the fhirclient Python library to interact with the FHIR API and perform CRUD operations on resources.
- User Data Storage: User credentials and other user-specific data are stored separately and securely in a local MySQL database.
- Data Flow: The app fetches medication and patient-related data from the FHIR server and associates it with user accounts stored in the MySQL database.

