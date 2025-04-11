import os
from dotenv import load_dotenv

load_dotenv()

class AuthConfig:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "YOUR_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")