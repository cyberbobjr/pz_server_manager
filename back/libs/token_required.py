import json
from functools import wraps

import jwt
from flask import jsonify, request

from back.libs import Config


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")

        if not token:
            message = jsonify({'message': 'a valid token is missing'})
            return message, 403
        secret = Config.app_config['auth']['secret']
        try:
            data = jwt.decode(token, secret, algorithms="HS256")
            current_user = {'username': 'toto'}
        except Exception as e:
            secret = Config.app_config['auth']['secret']
            good_token = jwt.encode({'username': 'toto'}, secret, algorithm='HS256')
            return jsonify({'message': good_token})
        return func(current_user, *args, **kwargs)

    return decorator
