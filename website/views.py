from flask import Blueprint, render_template, jsonify,request
from .models import db, Event,Booking
from flask_login import current_user

views = Blueprint('views' , __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('eventshome.html')

@views.route('/search', methods=['GET','POST'])
def search():
    return render_template('search.html')

@views.route('/profile',methods=['GET','POST'])
def profile():
    return render_template('profile.html')

@views.route('/bookings',methods=['GET','POST'])
def bookings():
    user_id = current_user.id
    user_bookings = Booking.query.filter_by(customer_id=user_id).all()
    return render_template('bookings.html',bookings=user_bookings)


@views.route('/buyTicket', methods=['GET','POST'])
def buyTicket():
    return render_template('organizer/create_event.html')

@views.route('/test', methods=['GET','POST'])
def settings():
    return render_template('order.html')

events_data = [
    {"id": 1, "name": "Concert", "date": "2025-05-01", "available_seats": 100, "price": 50},
    {"id": 2, "name": "Workshop", "date": "2025-06-15", "available_seats": 50, "price": 25},
]
