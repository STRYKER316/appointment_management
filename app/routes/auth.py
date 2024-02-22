from flask import Blueprint, request, jsonify
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

# User registration
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'Missing required data'}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    new_user = User(username=username, email=email, password=password)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})


# User login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'error': 'Missing required data'}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # We would want to use a more secure method for user authentication, such as JWT (JSON Web Tokens). This is dummy authentication :)
        return jsonify({'message': 'Login successful'})

    return jsonify({'error': 'Invalid username or password'}), 401
