from client import ACCESS_TOKEN
from client import CLIENT_ID
from client import CLIENT_SECRET
from nylas import APIClient

if __name__ == '__main__':
    test = CLIENT_ID
    nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token="JKGdsbS4aMucvo3achZfhxuuga6I5k"
    )

    response = nylas.calendars.delete("1sziuui6auwm4tzvxe2620vyd")
    print(response)
