from flask import Blueprint
from flask_restful import Api
from app.controllers.plan_controller import PlanResource


api = Blueprint("api", __name__)
rest_api = Api(api)

# Define Plan routes
rest_api.add_resource(
    PlanResource, "/plans", "/plans/<string:plan_id>"
)