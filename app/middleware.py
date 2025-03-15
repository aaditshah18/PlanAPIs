from functools import wraps
from flask import request, jsonify
from jsonschema import validate, ValidationError
from app.schemas import plan_schema


def validate_plan_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = request.get_json()
            validate(instance=data, schema=plan_schema)
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            return jsonify({"error": "Invalid JSON format"}), 400
        return func(*args, **kwargs)
    return wrapper