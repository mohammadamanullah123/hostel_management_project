<div align="center">
  <h1>🏠 Hostel Management System</h1>
  <p>A comprehensive Django-based solution for automating hostel administration and student management.</p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3.13-blue.svg?logo=python&logoColor=white" alt="Python Version" />
    <img src="https://img.shields.io/badge/Django-5.2.7-092E20.svg?logo=django" alt="Django Version" />
    <img src="https://img.shields.io/badge/Bootstrap-5.1.3-7952B3.svg?logo=bootstrap&logoColor=white" alt="Bootstrap" />
    <img src="https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite" alt="SQLite" />
  </p>
</div>

<br />

## 📖 Overview

The **Hostel Management System** replaces manual, paper-based processes with an efficient digital solution. It is designed to automate essential hostel administration tasks including:
- 🧑‍🎓 Student Management
- 🛏️ Room Allocation
- 📅 Attendance Tracking
- 📜 Hostel Rules Management

---

## 🚀 Technology Stack

### Backend
- **Framework:** Django 5.2.7
- **Language:** Python 3.13
- **Database:** SQLite (Development) / MySQL (Production)

### Frontend
- **HTML5** with Django Template Language
- **CSS3** & **Bootstrap 5.1.3**
- **JavaScript** for interactive elements

---

## 👥 User Roles & Features

### 👨‍💼 Admin Dashboard
- **Student Management:** Add, update, and delete student records.
- **Room Management:** Monitor availability and update capacity.
- **Allocations:** Seamlessly assign rooms to students.
- **Attendance:** Mark and view student daily attendance.
- **Rules:** Add and update hostel guidelines.

### 👨‍🎓 Student Portal
- **My Room:** View assigned room details.
- **My Attendance:** Check personal attendance records.
- **Guidelines:** Read and acknowledge hostel rules.
- **Profile:** Manage and update personal information.

---

## ⚙️ Installation & Setup

Follow these steps to get your development environment running:

### 1. Environment Setup

```bash
# Clone or create project directory
mkdir hostel_management_project
cd hostel_management_project

# Create & activate virtual environment
python -m venv hostel_env

# Windows:
.\hostel_env\Scripts\activate
# Mac/Linux:
source hostel_env/bin/activate

# Install required packages
pip install django mysqlclient
```

### 2. Run Development Server

```bash
# Navigate to the main project directory
cd hostel_management

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create an admin account (superuser)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

---

## 📁 Project Structure

<details>
<summary>Click to expand folder structure</summary>

```text
hostel_management_project/
├── hostel_env/                        # Virtual environment
└── hostel_management/                 # Main project folder
    ├── manage.py
    ├── db.sqlite3
    ├── static/                        # CSS, JS, Images
    ├── templates/                     # All HTML templates
    │   ├── base.html
    │   ├── auth/
    │   ├── students/
    │   ├── rooms/
    │   ├── attendance/
    │   └── rules/
    ├── hostel_management/             # Project configuration (settings.py, urls.py)
    ├── hostel_app/                    # Core application logic
    └── auth_app/                      # Authentication app
```
</details>

---

## 🗃️ Database Models

| Model | Description |
|---|---|
| **Students** | Stores comprehensive student information. |
| **Rooms** | Tracks room details, capacity, and availability. |
| **Attendance**| Daily attendance records for residents. |
| **HostelRules**| System rules and regulations data. |

---

## 🚀 Deployment Commands

<details>
<summary>Production Setup Basics</summary>

```bash
# Collect static files
python manage.py collectstatic

# Run with production settings (Requires configured production settings file)
python manage.py runserver --settings=hostel_management.settings.production
```
</details>

---

## 🎯 Default Access URLs

| Section | URL |
|---------|-----|
| 🏠 **Home Page** | `http://127.0.0.1:8000/` |
| 🛡️ **Admin Panel**| `http://127.0.0.1:8000/admin/` |
| 📊 **Student Dashboard**| `http://127.0.0.1:8000/dashboard/` |
| 🔑 **Login** | `http://127.0.0.1:8000/auth/login/` |
| 📝 **Register** | `http://127.0.0.1:8000/auth/register/` |

---

## 📞 Troubleshooting & Support

If you face any issues during setup:
1. Ensure your **virtual environment is activated** `(hostel_env)`.
2. Check if all required packages are installed (`pip freeze`).
3. Verify database migrations are applied without errors.
4. Make sure you run commands from inside the `hostel_management` folder (where `manage.py` is).

---
<div align="center">
  <i>Made with ❤️ for efficient Hostel Administration</i>
</div>

