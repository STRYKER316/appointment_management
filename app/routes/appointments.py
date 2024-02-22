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
            'title': appointment.title,
            'date': appointment.date.strftime('%Y-%m-%d'),
            'user_id': appointment.user_id
        }
        for appointment in appointments
    ]
    return jsonify({'appointments': appointment_list})


# Create an appointment
@appointments_bp.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()

    description = data.get('description')
    date_str = data.get('date')
    time_str = data.get('time')
    user_id = data.get('user_id')

    if not all([date_str, time_str, user_id]):
        return jsonify({'error': 'Missing required data'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    new_appointment = Appointment(description=description, date=date, time=time ,user_id=user_id)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment created successfully'})


# Get a single appointment
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


# # Availability of user on selected date
# @app.route('/availability', methods=['GET'])
# def check_availability():
#     user_id = request.args.get('user_id')
#     date = request.args.get('date')

#     for appointment in appointments:
#         if appointment['user_id'] == user_id and appointment['date'] == date:
#             return jsonify({'message': 'User not available on selected date'})
#     return jsonify({'message': 'User available on selected date'})