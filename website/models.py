from . import db

class Customer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120),unique=True)
    phone = db.Column(db.String(20),unique = True)
    location = db.Column(db.String(255))

    # relations

    bookings = db.relationship('booking',backref='customer')
    reviews = db.relationship('review',backref='customer')
    orders = db.relationship('order',backred='customer')