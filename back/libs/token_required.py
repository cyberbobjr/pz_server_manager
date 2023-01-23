import datetime
import jwt
from functools import wraps
from back.libs import Config


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        message = jsonify({'message': 'a valid token is missing'})
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")

        if not token:
            return message, 401

        secret = Config.app_config['auth']['secret']
        try:
            data = jwt.decode(token, secret, algorithms="HS256")
            expireIn = datetime.datetime.fromtimestamp(int(data["expireIn"]))
            if expireIn < datetime.datetime.now():
                return message, 401
            current_user = {'username': data["username"]}
        except Exception as e:
            message = jsonify({'message': 'a valid token is missing'})
            return message, 401
        return func(*args, **kwargs)

    return decorator
