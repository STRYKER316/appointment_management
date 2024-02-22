from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from app.routes import auth_bp, appointments_bp

app.register_blueprint(auth_bp)
app.register_blueprint(appointments_bp)