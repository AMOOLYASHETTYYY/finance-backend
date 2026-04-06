# Finance Data Processing & Access Control Backend

# Project Overview

This project is a backend system built using Flask that handles financial data processing with secure Role-Based Access Control (RBAC).

It provides REST APIs for:
- User authentication using JWT
- Financial record management (CRUD operations)
- Role-based authorization (Admin, Analyst, Viewer)
- Dashboard analytics for income, expense, and balance

The system ensures secure and controlled access to financial data based on user roles.

---

# Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite (default database)

---

# Key Features

## Authentication
- User registration
- Secure login using JWT tokens
- Token-based authentication for protected routes

## Role-Based Access Control (RBAC)
- Admin → Full access (users + records)
- Analyst → View records + dashboard
- Viewer → Dashboard only

## Financial Management
- Add income/expense records
- Update records
- Delete records
- Filter records by type, category, and date

## Dashboard
- Total income calculation
- Total expense calculation
- Balance computation

## User Management (Admin only)
- View all users
- Activate/deactivate users

---

# Database Models

## User
- id
- name
- email
- password
- role (admin / analyst / viewer)
- is_active

## FinancialRecord
- id
- user_id
- amount
- type (income / expense)
- category
- date
- notes

---

## Authentication Flow

1. User registers using `/register`
2. User logs in using `/login`
3. JWT token is generated
4. Token is required for all protected endpoints

---

# API Endpoints


## 📸 API Screenshots (Thunder Client Testing)

## Authentication

### Register Success
<img width="1217" height="533" alt="Screenshot 2026-04-06 161902" src="https://github.com/user-attachments/assets/33b9917b-95f4-4f4f-bc50-c355605243ed" />


### Register Validation
<img width="1175" height="478" alt="Screenshot 2026-04-06 161818" src="https://github.com/user-attachments/assets/cca6b91e-2926-49da-a8f1-69bb94f368ff" />

### Login Success
<img width="1229" height="492" alt="image" src="https://github.com/user-attachments/assets/b32b1510-fd1f-47eb-9860-9ef66ab6a7c3" />

### Login Failed
<img width="1207" height="523" alt="image" src="https://github.com/user-attachments/assets/610b6aa4-70fe-4b62-bdd0-406bfbf7e71c" />


## Protected Routes
### Dashboard Success
<img width="1092" height="534" alt="image" src="https://github.com/user-attachments/assets/e8c5c2fd-5af6-4c48-b79b-796e07c991b5" />

### Dashboard No Token
<img width="1114" height="502" alt="image" src="https://github.com/user-attachments/assets/deb4a0f8-2758-412d-a50f-b7f79a8c0b33" />


## Role-Based Access
### Admin Users
<img width="1238" height="920" alt="image" src="https://github.com/user-attachments/assets/f20be822-80e8-439a-b33c-f941ab22c507" />

### Active/Inactive Users
#### User is made inactive by admin
<img width="1028" height="539" alt="image" src="https://github.com/user-attachments/assets/5174fcf1-8a6d-463d-8a7d-e4507832cab7" />

#### User cannot log in
<img width="1124" height="362" alt="image" src="https://github.com/user-attachments/assets/a4c99a2a-70e7-4492-8f16-8c8d20a89fc7" />

#### Access denied
<img width="945" height="544" alt="image" src="https://github.com/user-attachments/assets/fd21045d-e003-4113-aa88-24d55ce155c9" />


## Financial Records
### Add Record
<img width="1204" height="554" alt="image" src="https://github.com/user-attachments/assets/6a3cfa3c-94fb-49e4-998f-37cb3cb3b320" />

### Validation Errors
#### Date Format
<img width="1182" height="529" alt="image" src="https://github.com/user-attachments/assets/1f655a1d-a217-4371-a668-27681ada345b" />

#### Amount
<img width="1146" height="519" alt="image" src="https://github.com/user-attachments/assets/d1c3f281-5273-4deb-bf86-5a439c9658bb" />

#### Incorrect Type
<img width="1144" height="520" alt="image" src="https://github.com/user-attachments/assets/40cf96ff-794b-48a8-a171-c1132a567b89" />

#### Category
<img width="995" height="509" alt="image" src="https://github.com/user-attachments/assets/70239cd7-721a-495e-8454-c5a3e59146d0" />

#### Access denied
<img width="951" height="488" alt="image" src="https://github.com/user-attachments/assets/eb7bb162-b59e-482b-a73b-8bb772c2bf19" />


## Filtered Records
#### All records
<img width="1073" height="621" alt="image" src="https://github.com/user-attachments/assets/f2b5685a-854c-4242-9205-08f4eb157d0d" />

#### Filter by category
<img width="1077" height="403" alt="image" src="https://github.com/user-attachments/assets/102f330b-cc50-4f46-92bb-0df87c0c912f" />

#### Filter by both category and Type
<img width="1066" height="443" alt="image" src="https://github.com/user-attachments/assets/a78c2322-a38f-4e22-930a-c9a086f4c3e9" />

#### Access denied
<img width="1041" height="501" alt="image" src="https://github.com/user-attachments/assets/2a1d4e0d-0751-4c17-b4fa-53a889df9cdb" />


### Delete Records
<img width="921" height="351" alt="image" src="https://github.com/user-attachments/assets/6bb3813f-0939-4650-a196-52f4d901b34b" />

#### Access denied
<img width="1052" height="551" alt="image" src="https://github.com/user-attachments/assets/027a01a4-a7b9-49c7-803f-7f21c6260f53" />


### Update Records
<img width="1155" height="401" alt="image" src="https://github.com/user-attachments/assets/d8479e35-c286-489f-bb28-43857e6e3cac" />

#### Access denied
<img width="957" height="519" alt="image" src="https://github.com/user-attachments/assets/aa51eb0f-04cb-4cfd-a361-9958a341e793" />


---
# Assumptions

Passwords are stored in plain text for simplicity

SQLite is used as lightweight database

No frontend is included (backend-only system)

JWT tokens are used for stateless authentication

---

# How to Run This Project

1. Clone the repository
    
git clone https://github.com/your-username/finance-backend.git

2. Create virtual environment

cd finance-backend
python -m venv venv

3. Activate virtual environment

-windows
venv\Scripts\activate
-mac/linux
source venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

5.Run

python app.py

6.Server will run at

http://127.0.0.1:5000/



