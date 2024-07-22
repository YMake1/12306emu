from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from src.database import models

deco_blu = Blueprint('deco_blu', __name__)

@deco_blu.route('/home/<user_id>')
@login_required
def home(user_id):
    if str(current_user.id) == user_id:
        return render_template('main/home.html', user_name=current_user.name)
    else:
        flash('You are not authorized to view this page.')
        return redirect(url_for('home', user_id=str(current_user.id)))
    
@deco_blu.route('/tickets/search', methods=['GET', 'POST'])
@login_required
def search():
    departure_name = request.args.get('departure')
    arrival_name = request.args.get('arrival')
    departure = models.Station.query.filter_by(name=departure_name).first()
    arrival = models.Station.query.filter_by(name=arrival_name).first()
    ticket_info = []
    if departure and arrival:
        departure_stops = models.Stop.query.filter_by(station_id=departure.id).all()
        arrival_stops = models.Stop.query.filter_by(station_id=arrival.id).all()
        train_ids = set(stop.train_id for stop in departure_stops) & set(stop.train_id for stop in arrival_stops)
        for train_id in train_ids:
            train = models.Train.query.get(train_id)
            if train:
                tickets = models.Ticket.query.filter_by(train_id=train.id).all()
                for ticket in tickets:
                    ticket_info.append({
                        "Train Number": train.train_number,
                        "Seat Type": ticket.seat_type,
                        "Price": ticket.price,
                        "Remaining": ticket.remaining
                    })
    return render_template('main/tickets.html', ticket_info=ticket_info)
