from flask import current_app as app, request, session, jsonify
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
        
class TokenResource(Resource):
    def get(self, user_id):
        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_address = request.remote_addr
        if 'user_id' in session and session['user_id'] == user_id:
            access_token = session.get('access_token')
            refresh_token = session.get('refresh_token')
            if access_token and refresh_token:
                app.logger.info(f"Tokens retrieved for user {user_id} {ip_address}")
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })
            else:
                return {'message': 'Tokens not found'}, 404
        else:
            return {'message': 'Unauthorized'}, 401