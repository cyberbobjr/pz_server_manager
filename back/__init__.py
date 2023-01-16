from flask import Flask, g

from back.routes import auth

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.add_url_rule("/test", view_func=auth.test)
    return app
