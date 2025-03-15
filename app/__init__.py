from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    from app.routes import api

    app.register_blueprint(api, url_prefix="/api/v1")

    return app
