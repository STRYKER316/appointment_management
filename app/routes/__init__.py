from flask import Flask

app = Flask(__name__)

from app.routes.auth import auth_bp
from app.routes.appointments import appointments_bp

app.register_blueprint(auth_bp)
app.register_blueprint(appointments_bp)
