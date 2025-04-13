# FinalYearProject_
PAM-HRIS (Privileged Access Management with HRIS Integration)

A centralized Django-based PAM system with department-specific access, role-based privilege management, and modular integration support.

Project Structure

pam_hris/: Core app handling authentication, role-based access control (RBAC), dashboard logic, and decorators.

hr_management/: HR-specific app with views restricted to HR users.

it_management/: IT-specific app with views restricted to IT users.

templates/: Shared HTML templates including base.html and role-specific dashboards.

docker-compose.yml: Defines Docker services for Django and MySQL.

manage.py: Django's main execution script.

.env: Environment variables for database and Django secret keys.

Core Features Implemented

Authentication System

Uses Django’s built-in login/logout views.

Superuser can be created via createsuperuser.

Custom User Privilege Models

User: Custom model storing name, email, password, and department flags (isHr, isIt).

UserPriviledgeGroup: Defines role groups such as Superuser, PrivilegedUser, and NormalUser.

UserPriviledge: Links each user to a specific privilege group.

Centralized Access Control

Decorators such as @it_required and @hr_required are defined in pam_hris/decorators.py.

Access control logic is shared across apps (e.g., HR and IT modules).

Role-Based Dashboard Routing

Central dashboard (main_dashboard.html) dynamically displays links based on user’s role and department.

Department dashboards are accessed via:

/it/dashboard/

/hr/dashboard/

Modular and Scalable Architecture

New apps (e.g., audit logs, business modules) can be added and protected using decorators.

Unified authentication and session management for all integrated apps.

Admin Interface

Models (User, UserPriviledge, UserPriviledgeGroup) are registered in Django admin.

Admin panel is accessible at /admin/.

Frontend Template Inheritance

base.html provides a shared layout.

All other templates extend this base layout for consistency.

How to Run

Start the services:

docker-compose up --build

Create a superuser:

docker-compose exec pam_server python manage.py createsuperuser

Access the app at:

Login page: http://localhost:8000/login/

Admin panel: http://localhost:8000/admin/

Upcoming Features

Integration with ELK stack for logging and security analysis.

Real-time alerting system for unauthorized access attempts.

Token-based API access and Single Sign-On (SSO) capability.

Expanded dashboards for department-specific data visualization.
