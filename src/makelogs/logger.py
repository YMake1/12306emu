import logging
from flask import Flask
from logging.handlers import RotatingFileHandler
from configs import cache_path, ensure_path_exists

def makelogs(app: Flask):
    if not app.debug:
        ensure_path_exists(cache_path, 'logs')
        ensure_path_exists(cache_path, 'errors')

        file_handler = RotatingFileHandler('cache/logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        error_handler = RotatingFileHandler('cache/errors/error.log', maxBytes=10240, backupCount=10)
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        error_handler.setLevel(logging.ERROR)
        app.logger.addHandler(error_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask startup')