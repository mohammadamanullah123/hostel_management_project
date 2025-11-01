🏠 Hostel Management System
📖 Overview
A comprehensive Hostel Management System built with Django that automates hostel administration tasks including student management, room allocation, attendance tracking, and hostel rules management. This system replaces manual paper-based processes with an efficient digital solution.

🚀 Technology Stack
Backend
Framework: Django 5.2.7

Language: Python 3.13

Database: SQLite (Development) / MySQL (Production)

Frontend
HTML5 with Django Template Language

CSS3 with Bootstrap 5.1.3

JavaScript for interactive elements

Development Tools
Virtual Environment: Python venv

Server: Django Development Server

IDE: VS Code

📁 Complete File Structure
text
hostel_management_project/
├── hostel_management/                 # Main project folder
│   ├── manage.py
│   ├── db.sqlite3
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── templates/                     # All HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── students/
│   │   │   └── list.html
│   │   ├── rooms/
│   │   │   └── list.html
│   │   ├── attendance/
│   │   │   └── list.html
│   │   └── rules/
│   │       └── list.html
│   ├── hostel_management/             # Project configuration
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── hostel_app/                    # Main application
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   │       └── __init__.py
│   └── auth_app/                      # Authentication app
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── views.py
│       ├── urls.py
│       └── migrations/
│           └── __init__.py
└── hostel_env/                        # Virtual environment
⚙️ Installation & Setup Commands
Step 1: Environment Setup
bash
# Create project directory
mkdir hostel_management_project
cd hostel_management_project

# Create virtual environment
python -m venv hostel_env

# Activate virtual environment
# Windows:
hostel_env\Scripts\activate
# Mac/Linux:
source hostel_env/bin/activate

# Install required packages
pip install django mysqlclient
Step 2: Project Creation
bash
# Create Django project
django-admin startproject hostel_management .
cd hostel_management

# Create applications
python manage.py startapp hostel_app
python manage.py startapp auth_app
Step 3: Database Setup
bash
# Create migrations
python manage.py makemigrations hostel_app

# migrations for entire program

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Follow prompts to create admin account
Step 4: Folder Structure Setup
bash
# Create static files folder
mkdir static
mkdir static\css

# Create templates folder structure
mkdir templates
mkdir templates\auth
mkdir templates\students
mkdir templates\rooms
mkdir templates\attendance
mkdir templates\rules
Step 5: Run Development Server
bash
# Start the development server
python manage.py runserver

# Access your application at:
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/admin/  (Admin panel)
🔧 Configuration Files
1. hostel_management/settings.py - Key Settings
python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hostel_app',
    'auth_app',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        # ... other settings
    },
]
2. URL Configuration
hostel_management/urls.py:

python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hostel_app.urls')),
    path('auth/', include('auth_app.urls')),
]

# 👥 User Roles & Features

# 👨‍💼 Admin Features

Add, update, and delete student records

Manage rooms (availability, capacity)

Assign rooms to students

Mark and view student attendance

Add and update hostel rules

# 👨‍🎓 Student Features

View assigned room details

Check personal attendance record

Read hostel rules

Update personal profile

# 🗃️ Database Models 

Main Tables:
Students - Student information

Rooms - Room details and availability

Attendance - Daily attendance records

HostelRules - Hostel rules and regulations

# 🚀 Deployment Commands
Development:
bash
# Run development server
python manage.py runserver

# Create new migrations when models change
python manage.py makemigrations

# Apply database changes
python manage.py migrate

# Create new admin user
python manage.py createsuperuser
Production (Basic):
bash
# Collect static files
python manage.py collectstatic

# Run with production settings
python manage.py runserver --settings=hostel_management.settings.production
📞 Support
For any issues during setup:

Ensure virtual environment is activated

Check all required packages are installed

Verify database migrations are applied

Confirm template and static file paths are correct

🎯 Default Access URLs
Home Page: http://127.0.0.1:8000/

Admin Panel: http://127.0.0.1:8000/admin/

Student Dashboard: http://127.0.0.1:8000/dashboard/

Login: http://127.0.0.1:8000/auth/login/

Register: http://127.0.0.1:8000/auth/register/

