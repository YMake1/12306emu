from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, current_user
from flask_restful import Api

from src.config.dev import DevelopmentConfig
from src.config.prod import ProductionConfig
from src.application.login import login_blu
from src.database.models import User, Station, Train, Stop, Ticket, Order, db
from src.design.resources import StationResource
from src.makelogs.logger import makelogs

def create_app(config_name):
    app = Flask(__name__)

    # globla config
    config = {
        'dev': DevelopmentConfig,
        'prop': ProductionConfig,
    }
    Config = config[f'{config_name}']
    app.config.from_object(Config)

    # login config
    app.register_blueprint(login_blu)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login_blu.login'
    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user
    @app.before_request
    def require_login():
        allowed_routes = ['login_blu.login', 'login_blu.signup']
        if request.endpoint not in allowed_routes and current_user.is_anonymous:
            return redirect(url_for('login_blu.login'))

    # database config
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # api config
    api = Api(app)
    api.add_resource(StationResource, '/stations/<int:station_id>', '/stations')

    # logger config
    makelogs(app)

    return app
