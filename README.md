# Appointment Management App

## Tools and Technologies:
* `Python3`
* `Flask`
* `Flask SQLAlchemy`
* `PostgreSQL`
* `psycopg2`


## Module Structures
* `app` - Application logic
    * `__init__.py` - Setting up the application
    * `models` - Database models
        * `user.py` - Users table model
        * `appointment.py` - Appointments table model
    * `routes` - API routes
        * `auth.py` - Signup, Login & Authentication APIs
        * `appointment.py` - CRUD APIs for managing appointments, User availabilty API
    * `config.py` - Configurations for the app
* `requirements.txt` - Python packages for the enviornment
* `run.py` - Script to run the app