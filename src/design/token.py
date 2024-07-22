from flask import Blueprint, request, jsonify
from functools import wraps
import jwt, datetime, pytz

from src.config.settings import Config

token_blu = Blueprint('token_blu', __name__)

def generate_tokens(username):
    utc_now = datetime.datetime.now(pytz.utc)
    access_token = jwt.encode({
        'user': username,
        'exp': utc_now + datetime.timedelta(minutes=15)
    }, Config.SECRET_KEY)
    refresh_token = jwt.encode({
        'user': username,
        'exp': utc_now + datetime.timedelta(days=7)
    }, Config.SECRET_KEY)
    return access_token, refresh_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            token = token.split(" ")[1]  # 提取Bearer后的token
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated