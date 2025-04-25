from flask import Blueprint, render_template, jsonify,request,flash,url_for,redirect
from website.models import db, Event,Booking,Venue,Category
from datetime import datetime
from website import db
from flask_login import login_required, current_user

events = Blueprint('events' , __name__)

@events.route('/events',methods=['GET'])
def get_events():
    events_conert = Event.query.all()
    return jsonify([{'id': event.id, 'name': event.name, 'date': event.date} for event in events_conert ]),200

@events.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['title']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        ticket_price = request.form.get('ticket_price', 0)
        available_seats = request.form.get('available_seats', 0)
        category_id = request.form.get('category_id')
        venue_id = request.form.get('venue_id')
        image = request.files.get('image')

        # Handle venue
        if request.form['venue_id'] == 'new':
            new_venue_name = request.form['new_venue']
            new_venue = Venue(name=new_venue_name, location=location, capacity=100)  # Default capacity or add more fields
            db.session.add(new_venue)
            db.session.flush()  # gets the ID without commit
            venue_id = new_venue.venue_id
        else:
            venue_id = request.form['venue_id']

        # Handle category
        if request.form['category_id'] == 'new':
            new_category_name = request.form['new_category']
            new_category = Category(name=new_category_name)
            db.session.add(new_category)
            db.session.flush()
            category_id = new_category.category_id
        else:
            category_id = request.form['category_id']

        try:
            event_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        except ValueError:
            flash('Invalid date or time format.', 'danger')
            return redirect(url_for('events.create_event'))

        # Optional: Save image and get URL/path
        #if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_event = Event(
                admin_id=current_user.id,  # assuming the user is an admin
                name=name,
                date=event_datetime,
                description=description,
                venue_id=venue_id,
                category_id=category_id,
                ticket_price=ticket_price,
                available_seats=available_seats
            ) 
        try:
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully','success')
            return redirect(url_for('admin.admin_home'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating event. Please try again','danger')
            print(e)

    venues = Venue.query.all()
    categories = Category.query.all()
    return render_template('organizer/create_event.html', venues=venues,categories=categories)

@events.route('/book-event', methods=['POST'])
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

@events.route('/cancel-booking', methods=['POST'])
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
