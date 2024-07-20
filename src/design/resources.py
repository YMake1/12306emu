from flask import current_app as app, request
from flask_restful import Resource

from src.database import models

class StationResource(Resource):
    def get(self, station_id=None):
        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_address = request.remote_addr
        if station_id:
            station = models.Station.query.get_or_404(station_id)
            app.logger.info(f"Station {station_id} retrieved {ip_address}")
            return station.to_dict()
        else:
            stations = models.Station.query.all()
            app.logger.info(f"All stations retrieved {ip_address}")
            return [station.to_dict() for station in stations]