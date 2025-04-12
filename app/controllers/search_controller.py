from flask import request
from flask_restful import Resource
from app.services.plan_service import PlanService
from app.middleware import verify_token

class SearchResource(Resource):
    """Resource for search operations"""
    
    @verify_token
    def get(self):
        """
        Search for plans based on query string.
        """
        try:
            query = request.args.get("q", "")
            return PlanService.search_plans(query)
        except Exception as e:
            return {"error": str(e)}, 500