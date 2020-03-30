import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
DEBUG = ENVIRONMENT == "dev"
HOST = '0.0.0.0' if ENVIRONMENT == "prod" else 'localhost'
API_URL = os.environ.get("API_URL", "http://localhost:5000/api")