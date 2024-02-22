import uuid

SECRET_KEY = uuid.uuid4().hex
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://testuser:testpass@localhost/appointmentappdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
