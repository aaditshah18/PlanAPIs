from flask import Flask
from flask_pymongo import PyMongo
from .config import Config
from elasticsearch import Elasticsearch

mongo = PyMongo()
es = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize Elasticsearch
    global es
    es = Elasticsearch(
        [app.config["ELASTICSEARCH_URI"]],
        basic_auth=(app.config.get("ELASTICSEARCH_USER", "elastic"), 
                   app.config.get("ELASTICSEARCH_PASSWORD", "GjU1EXbj68gNNIPk7+OB")),
        verify_certs=False  # For development only
    )
    
    # Check Elasticsearch connection
    if not es.ping():
        app.logger.warning("Elasticsearch connection failed")
    else:
        app.logger.info("Elasticsearch connected successfully")

    # Register Blueprints
    from app.app_routes import plan_bp, auth_bp
    app.register_blueprint(plan_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    return app