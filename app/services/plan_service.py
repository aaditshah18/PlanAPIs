from flask import request
from app import mongo
from http import HTTPStatus
from app.utils import generate_etag

class PlanService:
    @staticmethod
    def create_plan(data):
        """Creates a new plan if the plan_id does not already exist."""
        plan_id = data["objectId"]
        if mongo.db.plans.find_one({"objectId": plan_id}):
            return {"message": "Plan ID already exists."}, HTTPStatus.BAD_REQUEST

        mongo.db.plans.insert_one(data)
        new_plan = mongo.db.plans.find_one({"objectId": plan_id}, {"_id": 0})
        etag = generate_etag(new_plan)

        return {"message": "Plan stored successfully.", "plan": new_plan}, HTTPStatus.CREATED, {"ETag": etag}

    @staticmethod
    def get_plan(plan_id):
        """Retrieves a plan by its ID and includes ETag for caching."""
        plan = mongo.db.plans.find_one({"objectId": plan_id}, {"_id": 0})

        if not plan:
            return {"message": "Plan not found."}, HTTPStatus.NOT_FOUND

        etag = generate_etag(plan)

        # Handle If-None-Match for caching
        if request.headers.get("If-None-Match") == etag:
            return "", HTTPStatus.NOT_MODIFIED, {"ETag": etag}

        return plan, HTTPStatus.OK, {"ETag": etag}

    @staticmethod
    def delete_plan(plan_id):
        """Deletes a plan by its ID and returns appropriate status."""
        result = mongo.db.plans.delete_one({"objectId": plan_id})
        if result.deleted_count:
            return {"message": "Plan deleted."}, HTTPStatus.NO_CONTENT
        return {"message": "Plan not found."}, HTTPStatus.NOT_FOUND

    @staticmethod
    def update_plan(plan_id, data):
        """Updates a plan only if there is a change. Supports conditional read."""
        plan = mongo.db.plans.find_one({"objectId": plan_id}, {"_id": 0})

        if not plan:
            return {"message": "Plan not found."}, HTTPStatus.NOT_FOUND

        # Generate ETag for existing plan
        etag = generate_etag(plan)

        # Handle If-Match for conditional update
        if request.headers.get("If-Match") and request.headers["If-Match"] != etag:
            return {"message": "Plan has been modified by another process."}, HTTPStatus.PRECONDITION_FAILED

        # Check if there is no change in the update request
        if all(plan.get(k) == v for k, v in data.items()):
            return {"message": "No changes detected.", "plan": plan}, HTTPStatus.OK, {"ETag": etag}

        # Perform the update if there is a change
        mongo.db.plans.update_one({"objectId": plan_id}, {"$set": data})
        updated_plan = mongo.db.plans.find_one({"objectId": plan_id}, {"_id": 0})
        updated_etag = generate_etag(updated_plan)

        return {
            "message": "Plan updated successfully.",
            "plan": updated_plan
        }, HTTPStatus.OK, {"ETag": updated_etag}
