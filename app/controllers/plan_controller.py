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
            result = PlanService.create_plan(data)
            return result, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @verify_token
    def get(self, plan_id):
        """
        Retrieve a plan by ID (Requires authentication).
        """
        try:
            print(f"User: {request.user}")
            plan = PlanService.get_plan(plan_id)
            if plan:
                return plan, 200
            return {"error": "Plan not found"}, 404
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
            result = PlanService.update_plan(plan_id, data)
            if result:
                return result, 200
            return {"error": "Plan not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @verify_token
    def delete(self, plan_id):
        """
        Delete a plan by ID (Requires authentication).
        """
        try:
            result = PlanService.delete_plan(plan_id)
            if result:
                return result, 200
            return {"error": "Plan not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500