from flask import Blueprint
from flask_restful import Api
from app.controllers.plan_controller import PlanResource
from app.routes.auth import auth_bp

# Create Blueprints
plan_bp = Blueprint("plan", __name__)
api = Api(plan_bp)

# Register PlanResource with correct URL paths
api.add_resource(PlanResource, "/plans", "/plans/<string:plan_id>")

# Export Blueprints
__all__ = ["plan_bp", "auth_bp"]