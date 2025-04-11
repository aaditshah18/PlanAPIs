from flask import request
from flask_restful import Resource
from app.services.plan_service import PlanService
from app.middleware import validate_plan_json, verify_token

class PlanResource(Resource):
    """RESTful resource for handling Plan operations."""

    @verify_token
    @validate_plan_json
    def post(self):
        """
        Create a new plan (Requires authentication).
        """
        try:
            data = request.get_json()
            return PlanService.create_plan(data)  # Directly returning the service response
        except Exception as e:
            return {"error": str(e)}, 500

    @verify_token
    def get(self, plan_id):
        """
        Retrieve a plan by ID (Requires authentication).
        """
        try:
            print(f"User: {request.user}")
            return PlanService.get_plan(plan_id)  # Directly returning the service response
        except Exception as e:
            return {"error": str(e)}, 500

    @verify_token
    @validate_plan_json
    def patch(self, plan_id):
        """
        Update a plan conditionally (Requires authentication).
        """
        try:
            data = request.get_json()
            return PlanService.update_plan(plan_id, data)  # Directly returning the service response
        except Exception as e:
            return {"error": str(e)}, 500

    @verify_token
    def delete(self, plan_id):
        """
        Delete a plan by ID (Requires authentication).
        """
        try:
            return PlanService.delete_plan(plan_id)  # Directly returning the service response
        except Exception as e:
            return {"error": str(e)}, 500