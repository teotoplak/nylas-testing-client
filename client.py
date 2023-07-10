import os
from dotenv import load_dotenv
from nylas import APIClient

load_dotenv()


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

V3_CLIENT_ID_STAGING = os.getenv('V3_CLIENT_ID_STAGING')
V3_CLIENT_SECRET_STAGING = os.getenv('V3_CLIENT_SECRET_STAGING')
V3_API_KEY_STAGING = os.getenv('V3_API_KEY_STAGING')

V3_CLIENT_ID_PRODUCTION = os.getenv('V3_CLIENT_ID_PRODUCTION')
V3_CLIENT_SECRET_PRODUCTION = os.getenv('V3_CLIENT_SECRET_PRODUCTION')
V3_API_KEY_PRODUCTION = os.getenv('V3_API_KEY_PRODUCTION')

nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=ACCESS_TOKEN
    )
