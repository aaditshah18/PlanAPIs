import logging

from functools import wraps
from flask import request
from jsonschema import validate, ValidationError
from app.schemas import plan_schema
from google.auth.transport import requests as google_requests
from app.auth_config.auth_config import AuthConfig
from google.oauth2 import id_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_plan_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = request.get_json()
            validate(instance=data, schema=plan_schema)
        except ValidationError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Invalid JSON format"}, 400
        return func(*args, **kwargs)
    return wrapper

def no_payload(func):
    """
    Middleware to ensure no payload is sent in GET requests.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.query_string or request.get_json():
            return {"message": "Payload not allowed"}, 400
        return func(*args, **kwargs)
    return wrapper


def verify_token(func):
    """
    Middleware to verify the Google ID token.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                logger.warning("Unauthorized: Missing or invalid Authorization header")
                return {"message": "Token not found"}, 401

            token = auth_header.split(" ")[1]

            # Verify the ID token
            id_info = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                AuthConfig.GOOGLE_CLIENT_ID
            )

            if not id_info:
                logger.warning("Invalid token: No payload found")
                return {"message": "Invalid token"}, 401

            # Attach user info to the request
            request.user = id_info
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            return {"message": "Invalid token"}, 401
    return wrapper