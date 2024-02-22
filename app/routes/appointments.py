from flask import Blueprint, request, jsonify
from app import db
from app.models import Appointment
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

# Get all appointments
@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()

    appointment_list = [
        {
            'id': appointment.id,
            'date': appointment.date.strftime('%Y-%m-%d'),
            'time': appointment.time.strftime('%H:%M'),
            'description': appointment.description,
            'user_id': appointment.user_id
        }
        for appointment in appointments
    ]
    return jsonify({'appointments': appointment_list})


# Create an appointment
@appointments_bp.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    
    date_str = data.get('date')
    time_str = data.get('time')
    description = data.get('description')
    user_id = data.get('user_id')

    if not all([date_str, time_str, user_id]):
        return jsonify({'error': 'Missing required data'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    new_appointment = Appointment(date=date, time=time, description=description, user_id=user_id)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment created successfully'})


# Get details of a single appointment
@appointments_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    appointment_info = {
        'id': appointment.id,
        'description': appointment.description,
        'date': appointment.date.strftime('%Y-%m-%d'),
        'time': appointment.time.strftime('%H:%M'),
        'user_id': appointment.user_id
    }

    return jsonify({'appointment': appointment_info})


# Update an appointment
@appointments_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    data = request.get_json()

    description = data.get('description')
    date_str = data.get('date')
    time_str = data.get('time')
    user_id = data.get('user_id')

    if description:
        appointment.description = description

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointment.date = date
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    if time_str:
        try:
            time = datetime.strptime(time_str, '%H:%M').time()
            appointment.time = time
        except ValueError:
            return jsonify({'error': 'Invalid time format'}), 400

    if user_id:
        appointment.user_id = user_id

    db.session.commit()

    return jsonify({'message': 'Appointment updated successfully'})


# Delete an appointment
@appointments_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment deleted successfully'})


# Availability of user on a selected date
@appointments_bp.route('/availability', methods=['GET'])
def check_availability():
    # data = request.get_json()
    data = request.args

    user_id = data.get('user_id')
    date_str = data.get('date')

    print(user_id, date_str)

    if not all([user_id, date_str]):
        return jsonify({'error': 'Missing required data'}), 400

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Check if the user has any appointments on the selected date
    user_appointments = Appointment.query.filter_by(user_id=user_id, date=selected_date).all()

    if user_appointments:
        return jsonify({'message': 'User is not available on the selected date'})
    else:
        return jsonify({'message': 'User is available on the selected date'})
