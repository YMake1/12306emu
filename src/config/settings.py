import os
from dotenv import load_dotenv

class dataConfig():
    def __init__(self):
        load_dotenv('.devenv')

        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_host = os.getenv('DB_HOST')
        self.database = os.getenv('DB_DATABASE')

        self.redis_host = os.getenv('REDIS_HOST')
        self.redis_port = os.getenv('REDIS_PORT')
        self.redis_password = os.getenv('REDIS_PASSWORD')
        self.redis_poll = os.getenv('REDIS_POLL')

data = dataConfig()

db_user = data.db_user
db_password = data.db_password
db_host = data.db_host
database = data.database

redis_host = data.redis_host
redis_port = data.redis_port
redis_password = data.redis_password
redis_poll = data.redis_poll

class Config(object):
    DEBUG=False
    LOG_LEVEL = "INFO"
    SECRET_KEY = 'your secret key'
    JSON_AS_ASCII = False
    REDIS_HOST = redis_host
    REDIS_PORT = redis_port
    REDIS_PASSWORD = redis_password
    REDIS_POLL = redis_poll
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{database}?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE=10
    SQLALCHEMY_POOL_TIMEOUT=10
    SQLALCHEMY_MAX_OVERFLOW=2
    RABBITUSER="user"
    RABBITPASSWORD="db_password"
    RABBITHOST="your ip"
    RABBITPORT="your port"