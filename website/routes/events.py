from flask import Blueprint, render_template, jsonify,request,flash,url_for,redirect
from website.models import db, Event,Booking,Venue,Category
from datetime import datetime
from website import db
from flask_login import login_required, current_user
from geopy.distance import geodesic

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


        try:
            if category_id:
                category_id = int(category_id)
            else:
                category_id = None  # Or a default value if needed
        except ValueError:
            flash('Invalid category selected.', 'danger')
            return redirect(url_for('events.create_event'))

        # Handle venue
        if request.form['venue_id'] == 'new':
            new_venue_name = request.form['new_venue']
            new_venue = Venue(name=new_venue_name, location=location, capacity=100)  # Default capacity or add more fields
            db.session.add(new_venue)
            db.session.flush()  # gets the ID without commit
            venue_id = new_venue.venue_id
        else:
            venue_id = request.form['venue_id']

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
    return render_template('organizer/create_event.html', venues=venues)

@events.route('/category/<int:category_id>')
def category_events(category_id):
    # Get the category
    category = Category.query.get_or_404(category_id)
    
    # Get all events in this category
    events = Event.query.filter_by(category_id=category_id).all()
    
    return render_template('category_events.html', 
                          category=category, 
                          events=events)

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

@events.route('/search-events', methods=['GET'])
def search_events():
    location = request.args.get('location')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    # Assume you have a list of events with lat/lon fields
    events = Event.query.all()  # get all events first

    user_location = None
    if latitude and longitude:
        user_location = (float(latitude), float(longitude))
    elif location:
        # Optionally: you can geocode the 'location' name into lat/lon (using geopy/Nominatim)
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="event_app")
        loc = geolocator.geocode(location)
        if loc:
            user_location = (loc.latitude, loc.longitude)

    if user_location:
        # Annotate events with distance
        events_with_distance = []
        for event in events:
            event_location = (event.latitude, event.longitude)
            distance = geodesic(user_location, event_location).km
            events_with_distance.append((event, distance))

        # Sort events by distance
        events_with_distance.sort(key=lambda x: x[1])

        # Only keep the event objects (or you can send distance if you want)
        sorted_events = [event for event, dist in events_with_distance]
    else:
        # No location info, show all events
        sorted_events = events

    return render_template('search_results.html', events=sorted_events)


@events.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '')

    # For example, match locations or events
    matching_locations = Event.query.filter(Event.name.ilike(f"%{query}%")).limit(5).all()
    suggestions = [event.name for event in matching_locations]

    # You can also include locations/venues separately if you have them
    
    return jsonify({'suggestions': suggestions})

@events.route('/event/<int:event_id>/book', methods=['GET', 'POST'])
def book_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        number_of_tickets = int(request.form.get('number_of_tickets'))

        if number_of_tickets < 1:
            flash('Please select at least 1 ticket.', 'danger')
            return redirect(url_for('book_event', event_id=event_id))

        total_price = event.ticket_price * number_of_tickets

        # Create the booking
        booking = Booking(
            event_id=event.event_id,
            booking_name=event.name,
            booking_date=event.date,
            num_tickets=number_of_tickets,
            customer_id=current_user.id,
            total_price=total_price
        )

        db.session.add(booking)
        db.session.commit()

        flash(f'Booked {number_of_tickets} tickets successfully!', 'success')
        return redirect(url_for('views.bookings'))

    return render_template('book_event.html', event=event)

@events.route('/event/<int:event_id>')
def event_details(event_id):
    # Get the event or return 404 if not found
    event = Event.query.get_or_404(event_id)
    
    # Get the venue information
    venue = Venue.query.get(event.venue_id)

    related_events = Event.query.filter_by(category_id=event.category_id)\
                          .filter(Event.event_id != event.event_id)\
                          .limit(3)\
                          .all()
    
    # You could also fetch related information here
    # For example: reviews, comments, similar events, etc.
    
    return render_template('event_details.html', 
                          event=event, 
                          venue=venue,
                           related_events=related_events)


