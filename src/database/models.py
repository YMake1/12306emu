from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime, pytz

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    id_number = db.Column(db.String(18), unique=True, nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt', salt_length=4)
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(pytz.utc))

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    passenger_type = db.Column(db.String(1), nullable=False) # 0:adult 1:child 2:student
    id_number = db.Column(db.String(18), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    city = db.Column(db.String(64), nullable=False)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city
        }

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_number = db.Column(db.String(64), unique=True, nullable=False)
    start_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    end_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    situation = db.Column(db.String(1), nullable=False) # 0:normal 1:stop 2:delay

class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    seat_type = db.Column(db.String(1), nullable=False) # 0:hardseat or second 1:hardbed or first 2:softbed or commercial
    price = db.Column(db.Float, nullable=False)
    remaining = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)