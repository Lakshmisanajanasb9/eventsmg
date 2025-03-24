from flask import Blueprint, render_template, jsonify,request
from .models import db, Event,Booking

views = Blueprint('views' , __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('eventshome.html')


@views.route('/example', methods=['GET', 'POST'])
def example():
    return render_template('example.html')

events_data = [
    {"id": 1, "name": "Concert", "date": "2025-05-01", "available_seats": 100, "price": 50},
    {"id": 2, "name": "Workshop", "date": "2025-06-15", "available_seats": 50, "price": 25},
]

@views.route('/events',methods=['GET'])
def get_events():
    events_conert = Event.query.all()
    return jsonify([{'id': event.id, 'name': event.name, 'date': event.date} for event in events_conert ]),200

@views.route('/book-event', methods=['POST'])
def book_event():
    data = request.get_json()
    event_id = data.get('event_id')
    customer_id = data.get('customer_id')
    num_tickets = data.get('num_tickets')

    if not event_id or not num_tickets or not customer_id:
        return jsonify({'error': 'Event ID and number of tickets are required'}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    if event.available_seats < num_tickets:
        return jsonify({'error': 'Not enough available seats'}), 400

    # Reduce available seats
    event.available_seats -= num_tickets
    
    # Create a new booking
    booking = Booking(event_id=event.id, num_tickets=num_tickets)
    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': 'Booking successful', 'event': event.name, 'tickets_booked': num_tickets}), 200

@views.route('/cancel-booking', methods=['POST'])
def cancel_booking():
    data = request.get_json()
    booking_id = data.get('booking_id')

    if not booking_id:
        return jsonify({'error': 'Booking ID is required'}), 400

    # Find the booking
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    # Find the event and restore available seats
    event = Event.query.get(booking.event_id)
    if event:
        event.available_seats += booking.num_tickets  # Restore the seats

    # Remove the booking
    db.session.delete(booking)
    db.session.commit()

    return jsonify({'message': 'Booking canceled successfully'}), 200