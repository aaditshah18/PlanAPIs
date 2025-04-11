from flask import redirect, url_for, session, request, jsonify
from flask_login import login_user, logout_user
from requests_oauthlib import OAuth2Session
import jwt
from jwt import PyJWKClient
from app.auth_config.auth_config import AuthConfig
from app.models import User
from app import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWK Client for token validation
jwks_client = PyJWKClient(AuthConfig.GOOGLE_JWKS_URL)

def login():
    google = OAuth2Session(AuthConfig.GOOGLE_CLIENT_ID, redirect_uri=AuthConfig.GOOGLE_REDIRECT_URI, scope=['openid', 'email', 'profile'])
    authorization_url, state = google.authorization_url(AuthConfig.GOOGLE_AUTH_URL, access_type="offline", prompt="consent")
    session['oauth_state'] = state
    return redirect(authorization_url)

def callback():
    if 'oauth_state' not in session or request.args.get('state') != session['oauth_state']:
        return jsonify({'error': 'Invalid state parameter'}), 401

    try:
        google = OAuth2Session(AuthConfig.GOOGLE_CLIENT_ID, redirect_uri=AuthConfig.GOOGLE_REDIRECT_URI, state=session['oauth_state'])
        token = google.fetch_token(AuthConfig.GOOGLE_TOKEN_URL, client_secret=AuthConfig.GOOGLE_CLIENT_SECRET, authorization_response=request.url)
    except Exception as e:
        logger.error(f'OAuth token fetch failed: {str(e)}')
        return jsonify({'error': 'OAuth token fetch failed'}), 401

    # Store tokens in session
    session['oauth_token'] = token
    access_token = token['access_token']
    refresh_token = token.get('refresh_token')

    # Validate the ID token (signed by Google using RS256)
    id_token = token.get('id_token')
    if id_token:
        try:
            decoded_token = validate_google_token(id_token)
            user_info = {
                'email': decoded_token['email'],
                'name': decoded_token.get('name'),
                'sub': decoded_token['sub']
            }

            # Create or log in the user
            user = User.query.filter_by(email=user_info['email']).first()
            if not user:
                user = User(email=user_info['email'], name=user_info['name'])
                db.session.add(user)
                db.session.commit()
            login_user(user)

            # Return tokens (for demonstration purposes)
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_info': user_info
            })
        except ValueError as e:
            logger.error(f'Token validation failed: {str(e)}')
            return jsonify({'error': str(e)}), 401

    return jsonify({'error': 'Failed to authenticate'}), 401

def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))

def validate_google_token(id_token):
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
        decoded_token = jwt.decode(id_token, signing_key.key, algorithms=["RS256"], audience=AuthConfig.GOOGLE_CLIENT_ID)
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")