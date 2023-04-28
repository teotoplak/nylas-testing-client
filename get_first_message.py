from client import ACCESS_TOKEN
from client import CLIENT_ID
from client import CLIENT_SECRET
from nylas import APIClient

if __name__ == '__main__':
    test = CLIENT_ID
    nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=ACCESS_TOKEN
    )

    response = nylas.calendars.all()
    print(response)
