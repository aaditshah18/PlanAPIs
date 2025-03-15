import logging
from flask import Blueprint, redirect, request, jsonify
from app.auth_config.auth_config import AuthConfig
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/authorize")
def authorize():
    """
    Redirects the user to Google's OAuth consent page.
    """
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={AuthConfig.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={AuthConfig.GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=email profile"
    )
    return redirect(auth_url)

@auth_bp.route("/callback")
def callback():
    """
    Handles the OAuth callback from Google and returns the token.
    """
    try:
        code = request.args.get("code")
        if not code:
            logger.warning("Authorization code not found")
            return jsonify({"message": "Authorization code not found"}), 400

        # Exchange the authorization code for tokens
        token_response = id_token.verify_oauth2_token(
            code,
            google_requests.Request(),
            AuthConfig.GOOGLE_CLIENT_ID
        )

        # Extract user info from the token
        id_info = token_response

        # Return the token and user info
        return jsonify({
            "token": token_response["id_token"],
            "expiresIn": token_response["expiry_date"],
            "tokenType": "Bearer",
            "user": {
                "email": id_info["email"],
                "name": id_info.get("name", ""),
                "picture": id_info.get("picture", "")
            }
        })
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        return jsonify({"message": "Authentication failed"}), 500