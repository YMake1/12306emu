from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(3), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    city = db.Column(db.String(64), nullable=False)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_number = db.Column(db.String(64), unique=True, nullable=False)
    start_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    end_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    seat_type = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    remaining = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)