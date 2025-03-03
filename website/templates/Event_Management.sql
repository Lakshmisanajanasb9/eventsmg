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
);