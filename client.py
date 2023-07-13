import os
from dotenv import load_dotenv
from nylas import APIClient

load_dotenv()


V2_CLIENT_ID = os.getenv('V2_CLIENT_ID')
V2_CLIENT_SECRET = os.getenv('V2_CLIENT_SECRET')
V2_ACCESS_TOKEN = os.getenv('V2_ACCESS_TOKEN')

V3_CLIENT_ID_STAGING = os.getenv('V3_CLIENT_ID_STAGING')
V3_CLIENT_SECRET_STAGING = os.getenv('V3_CLIENT_SECRET_STAGING')
V3_API_KEY_STAGING = os.getenv('V3_API_KEY_STAGING')

V3_CLIENT_ID_PRODUCTION = os.getenv('V3_CLIENT_ID_PRODUCTION')
V3_CLIENT_SECRET_PRODUCTION = os.getenv('V3_CLIENT_SECRET_PRODUCTION')
V3_API_KEY_PRODUCTION = os.getenv('V3_API_KEY_PRODUCTION')

nylas = APIClient(
        client_id=V2_CLIENT_ID,
        client_secret=V2_CLIENT_SECRET,
        access_token=V2_ACCESS_TOKEN
    )
