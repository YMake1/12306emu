import os
from dotenv import load_dotenv

class dataConfig():
    def __init__(self):
        load_dotenv('.devenv')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.database = os.getenv('DB_DATABASE')

data = dataConfig()
user = data.user
password = data.password
host = data.host
database = data.database

class Config(object):
    DEBUG=False
    LOG_LEVEL = "INFO"
    REDIS_HOST = 'your host'
    REDIS_PORT = 'your port'
    REDIS_PASSWORD = 'your password'
    REDIS_POLL = 10
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE=10
    SQLALCHEMY_POOL_TIMEOUT=10
    SQLALCHEMY_MAX_OVERFLOW=2
    RABBITUSER="user"
    RABBITPASSWORD="password"
    RABBITHOST="your ip"
    RABBITPORT="your port"