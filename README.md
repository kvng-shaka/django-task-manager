# Django Task Manager

A full-stack task management web application built with **Python and Django**. The project allows users to create, manage, organize, and track their tasks through a secure, user-specific dashboard.

## Features

* User registration and authentication
* Automatic login after registration
* User-specific task ownership
* Create, view, edit, and delete tasks
* Secure task access and authorization
* Search tasks by title or description
* Filter tasks by status
* Filter tasks by priority
* Dashboard task statistics
* Task completion progress tracking
* User profile
* Edit profile information
* Change password
* Responsive interface
* Delete confirmation modal

## Tech Stack

* **Python**
* **Django**
* **SQLite**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Git & GitHub**

## Project Structure

```text
task_manager/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tasks/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── registration/
│   └── tasks/
│
├── static/
│   └── css/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kvng-shaka/django-task-manager.git
cd django-task-manager
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Task Management

Authenticated users can:

* Create new tasks
* Set task status
* Set task priority
* Add descriptions
* Edit tasks
* Delete tasks
* Search tasks
* Filter tasks
* Track completion progress

Each task belongs to the user who created it, preventing users from accessing or modifying other users' tasks.

## Authentication & Security

The application uses Django's built-in authentication system.

Protected functionality includes:

* Login-required pages
* User-specific task queries
* Ownership checks for task details
* Ownership checks for editing
* Ownership checks for deletion
* Secure password management

## Dashboard

The dashboard provides an overview of the user's tasks, including:

* Total tasks
* Completed tasks
* In-progress tasks
* Pending tasks
* Completion percentage
* Visual progress bar

## Future Improvements

Planned improvements include:

* Task due-date management
* Overdue task indicators
* Improved task status controls
* User profile customization
* Notifications
* Pagination
* REST API
* Automated tests
* Production deployment
* PostgreSQL database
* Cloud media storage

## Author

**Kvng Shaka**

Built as a practical project for developing and demonstrating Python and Django web development skills.
