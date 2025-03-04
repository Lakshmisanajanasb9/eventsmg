from flask import Blueprint, render_template, jsonify
from .models import db, Event 

views = Blueprint('views' , __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


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
    return jsonify([{'id': event.id, 'name': event.name, 'date': event.date} for event in events_conert]),200
