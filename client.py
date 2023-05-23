import os
from dotenv import load_dotenv
from nylas import APIClient

load_dotenv()


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

V3_CLIENT_ID = os.getenv('V3_CLIENT_ID')
V3_CLIENT_SECRET = os.getenv('V3_CLIENT_SECRET')
V3_API_KEY = os.getenv('V3_API_KEY')

nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=ACCESS_TOKEN
    )
