from . import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120),unique=True)
    phone = db.Column(db.String(20),unique = True)
    location = db.Column(db.String(255))
     # relations
    bookings = db.relationship('booking',backref='customer')
    reviews = db.relationship('review',backref='customer')
    orders = db.relationship('order',backref ='customer')


class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer,  nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)
    #relations
    category = db.relationship('Category', backref='events')

class Venue(db.Model):
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)  
    capacity = db.Column(db.Integer, nullable=False)  
    description = db.Column(db.Text)
     events = db.relationship('Event', backref='venue')

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)


class Performer(db.Model):  
    __tablename__ = 'performer'
    performer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

class Booking(db.Model):
    __tablename__ = 'booking'
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    customer = db.relationship('Customer', backref='bookings')
    event = db.relationship('Event', backref='bookings')

class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=True)  # Optional
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), nullable=True)  # Optional
    performer_id = db.Column(db.Integer, db.ForeignKey('performer.performer_id'), nullable=True)  # Optional
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5 stars
    comment = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10,2), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')  # Pending, Confirmed, Canceled

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

"""

CREATE DATABASE Event_Management;
USE Event_Management;

CREATE TABLE Admins ( --add performer
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL
);


CREATE TABLE Venues (
    venue_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    capacity INT NOT NULL,
    description TEXT
);

CREATE TABLE Events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT NOT NULL,
    venue_id INT NOT NULL,
    'name' VARCHAR(255) NOT NULL,
    'date' DATETIME NOT NULL,
    'description' TEXT,
    'ticket_price' DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES Admins(admin_id),
    FOREIGN KEY (venue_id) REFERENCES Venues(venue_id) 
);  """