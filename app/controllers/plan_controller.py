from flask import request
from flask_restful import Resource
from app.services.plan_service import PlanService
from app.middleware import validate_plan_json

class PlanResource(Resource):
    @validate_plan_json
    def post(self):
        return PlanService.create_plan(request.get_json())

    def get(self, plan_id):
        return PlanService.get_plan(plan_id)

    @validate_plan_json
    def patch(self, plan_id):
        return PlanService.update_plan(plan_id, request.get_json())

    def delete(self, plan_id):
        return PlanService.delete_plan(plan_id)
