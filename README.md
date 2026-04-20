# Smart-Parking-Management-System
### A Scalable Full-Stack Parking Automation Platform
A full-stack web-based application designed to efficiently manage parking spaces in real time. This system allows users to view available parking slots, book spaces online, and manage reservations seamlessly, while administrators can monitor occupancy, pricing, and usage analytics.

## Overview
The Smart Parking Management System is a production-style full-stack web application designed to automate parking operations using real-time slot tracking, booking management, and billing automation.
It simulates a real-world intelligent parking ecosystem, demonstrating strong skills in:

- System Design
- Backend Engineering
- Database Architecture
- Full-stack Web Development
## Key Highlights
-  Real-time parking slot allocation
-  Secure authentication system
-  Admin-controlled monitoring dashboard
-  Automated entry/exit tracking
-  Dynamic billing system
-  Fully responsive UI

## System Architecture
![System Architecture](https://github.com/Shashank123-wq-tech/Smart-Parking-Management-System/blob/main/image.png)

## System Workflow
![System Workflow](https://github.com/Shashank123-wq-tech/Smart-Parking-Management-System/blob/main/mermaid-diagram%20(2).png) 

## Architecture Explanation
The system follows a 3-tier architecture:

### Presentation Layer (Frontend)
Built using HTML, CSS, Bootstrap, JavaScript.
Handles user interaction and UI rendering.
Displays real-time parking availability.

### Application Layer (Backend)
Developed using Flask.
Handles authentication, booking logic, billing system.
Exposes REST APIs for frontend communication

### Data Layer (Database)
Stores user data, bookings, and transaction history
Ensures data integrity and relational consistency
Deployment
## Local Deployment
### Clone repository
git clone https://github.com/your-username/smart-parking-system.git

### Move into directory
cd smart-parking-system

### Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

### Install dependencies
pip install -r requirements.txt

### Run application
python app.py

## Cloud Deployment (Render / Railway / AWS)
### Steps for Deployment:
1)Push project to GitHub.

2) Connect repository to Render.

3) Set environment variables.

4) Add start command:(gunicorn app:app). 
5) Deploy and get live URL: https://smart-parking-management-system-1-y2mi.onrender.com

## UI Preview :
### Home Page
![HomePage](https://github.com/Shashank123-wq-tech/Smart-Parking-Management-System/blob/main/Screenshot%202026-04-20%20230915.png) 
![UI](https://github.com/Shashank123-wq-tech/Smart-Parking-Management-System/blob/main/Screenshot%202026-04-20%20231500.png)

 ## Future Improvements
- AI-based parking prediction system
- QR / Barcode entry system
- Payment gateway integration
- IoT sensor-based slot detection
- Android/iOS mobile application
## Key Learnings
- Full-stack system design from scratch
- REST API development and integration
- Database schema design & optimization
- Real-world workflow simulation
- Deployment of Python web applications

## Developer

### Shashank Dixit
### M.Sc. Data Science & Artificial Intelligence
### IIITM Gwalior
