from flask_restful import Resource

from src.database import models

class StationResource(Resource):
    def get(self, station_id=None):
        if station_id:
            station = models.Station.query.get_or_404(station_id)
            return station.to_dict()
        else:
            stations = models.Station.query.all()
            return [station.to_dict() for station in stations]