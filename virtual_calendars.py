import requests
from nylas import APIClient

from client import CLIENT_ID
from client import CLIENT_SECRET


def create_nylas_account(key="api-testing"):
    content = {
        "client_id": CLIENT_ID,
        "provider": "nylas",
        "scopes": "calendar",
        "email": key,
        "name": "Virtual Calendar",
        "settings": {}
    }

    # Post the authentication payload to Nylas.
    nylas_authorization = requests.post(
        "https://api.nylas.com/connect/authorize", json=content
    )
    nylas_code = nylas_authorization.json()["code"]

    register_content = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": nylas_code
    }

    registering_account = requests.post(
        "https://api.nylas.com/connect/token", json=register_content
    )

    return registering_account.json()['account_id'], registering_account.json()['access_token']


def create_virtual_calendar(access_token):
    nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=access_token
    )
    calendar = nylas.calendars.create()
    calendar.name = "My New Calendar"
    calendar.description = "Description of my new calendar"
    calendar.location = "Location description"
    calendar.timezone = "America/Los_Angeles"
    calendar.save()
    return calendar.id


def get_all_calendars(account_id, access_code):
    nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=access_code
    )
    return nylas.calendars.all()


if __name__ == '__main__':
    account_id, access_code = create_nylas_account()
    print(f"created account {account_id} with access code {access_code}")
    existing_calendars = get_all_calendars(account_id, access_code)
    print(f"num of existing calendars after creation of account: {existing_calendars}")
    calendar_id = create_virtual_calendar(access_code)
    print(f"created calendar {calendar_id}")

    # cleanup
    nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=access_code
    )
    nylas.calendars.delete(calendar_id)
    nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        # access_token=access_code
    )
    nylas.accounts.delete(account_id)

