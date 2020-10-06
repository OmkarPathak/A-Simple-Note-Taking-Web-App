from flask import Flask
from flask_restful import Api
from flask_pagedown import PageDown
import os

api = Api()
pagedown = PageDown()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    # extensions
    api.init_app(app)
    pagedown.init_app(app)

    from core import core
    app.register_blueprint(core)

    return app
