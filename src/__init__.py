import click
from rich import print
from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, current_user
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate

from src.config.dev import DevelopmentConfig
from src.config.prod import ProductionConfig
from src.application.login import login_blu
from src.application.error import error_blu
from src.application.decoration import deco_blu
from src.database.models import User, Station, Train, Stop, Ticket, Order, db
from src.database.views import initdb
from src.design.resources import StationResource, TokenResource
from src.makelogs.logger import makelogs

def create_app(config_name):
    app = Flask(__name__)

    # globla config
    config = {
        'dev': DevelopmentConfig,
        'prop': ProductionConfig,
    }
    Config = config[f'{config_name}']
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    CORS(app, resources={r"/login": {"origins": "*"}, r"/api/*": {"origins": "*"}})
    app.config.from_object(Config)

    # blueprint config
    app.register_blueprint(login_blu)
    app.register_blueprint(error_blu)
    app.register_blueprint(deco_blu)

    # login config
    login_manager = LoginManager(app)
    login_manager.login_view = 'login_blu.login'
    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user
    @app.before_request
    def require_login():
        print(request.endpoint)
        allowed_routes = ['login_blu.login', 'login_blu.signup', 'stationresource']
        if request.endpoint not in allowed_routes and current_user.is_anonymous:
            return redirect(url_for('login_blu.login'))

    # database config
    migrate = Migrate(app, db)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # api config
    api = Api(app)
    api.add_resource(StationResource, '/api/stations/<int:station_id>', '/api/stations')
    api.add_resource(TokenResource, '/api/tokens/<int:user_id>')

    # logger config
    makelogs(app)

    # command config
    @app.cli.command('initdb')
    @click.option('--station', is_flag=True, help='Importing station data')
    def initdb_command(station):
        initdb(station)

    return app
