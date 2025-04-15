from flask import Blueprint, render_template, jsonify,request
from .models import db, Event,Booking

views = Blueprint('views' , __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('eventshome.html')

@views.route('/search', methods=['GET','POST'])
def search():
    return render_template('search.html')

@views.route('/example', methods=['GET', 'POST'])
def example():
    return render_template('example.html')

events_data = [
    {"id": 1, "name": "Concert", "date": "2025-05-01", "available_seats": 100, "price": 50},
    {"id": 2, "name": "Workshop", "date": "2025-06-15", "available_seats": 50, "price": 25},
]

