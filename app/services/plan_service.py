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
        """Retrieves a plan with ETag support for caching."""
        plan = mongo.db.plans.find_one({"objectId": plan_id}, {"_id": 0})
        if not plan:
            return {"message": "Plan not found."}, HTTPStatus.NOT_FOUND

        etag = generate_etag(plan)

        # Handle If-None-Match for caching
        if request.headers.get("If-None-Match") == etag:
            return {"message": "Not modified."}, HTTPStatus.NOT_MODIFIED, {"ETag": etag}

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
        """Updates a plan only if there is a change. Supports conditional read and write."""
        plan = mongo.db.plans.find_one({"objectId": plan_id}, {"_id": 0})
        if not plan:
            return {"message": "Plan not found."}, HTTPStatus.NOT_FOUND

        # Generate ETag for existing plan
        etag = generate_etag(plan)

        # Handle If-Match for concurrency control
        if "If-Match" in request.headers and request.headers["If-Match"] != etag:
            return {"message": "Plan has been modified by another process."}, HTTPStatus.PRECONDITION_FAILED

        # Check if the update request contains changes
        if all(plan.get(k) == v for k, v in data.items()):
            return {"message": "No changes detected.", "plan": plan}, HTTPStatus.OK, {"ETag": etag}

        # Recursively handle objectId changes
        def handle_object_id_changes(original, updated):
            if isinstance(original, dict) and isinstance(updated, dict):
                for key, value in updated.items():
                    if key == "objectId" and key in original and original[key] != value:
                        # Preserve the original object with the new objectId
                        original[key] = value
                    elif key in original:
                        # Recursively handle nested fields
                        original[key] = handle_object_id_changes(original[key], value)
                    else:
                        # Add new fields
                        original[key] = value
                return original
            elif isinstance(original, list) and isinstance(updated, list):
                # Handle lists (e.g., linkedPlanServices)
                for updated_item in updated:
                    if isinstance(updated_item, dict) and "objectId" in updated_item:
                        # Check if the object already exists in the original list
                        existing_item = next(
                            (item for item in original if item.get("objectId") == updated_item["objectId"]), None
                        )
                        if existing_item:
                            # Update the existing object
                            handle_object_id_changes(existing_item, updated_item)
                        else:
                            # Add the new object to the list
                            original.append(updated_item)
                return original
            else:
                # Return updated value if types don't match
                return updated

        # Apply the logic to the plan and data
        updated_plan = handle_object_id_changes(plan, data)

        # Perform the update
        mongo.db.plans.update_one({"objectId": plan_id}, {"$set": updated_plan})
        updated_plan = mongo.db.plans.find_one({"objectId": plan_id}, {"_id": 0})
        updated_etag = generate_etag(updated_plan)

        return {
            "message": "Plan updated successfully.",
            "plan": updated_plan
        }, HTTPStatus.OK, {"ETag": updated_etag}
