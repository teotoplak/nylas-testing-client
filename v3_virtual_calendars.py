import requests
from client import V3_API_KEY

DOMAIN = "https://api-staging.us.nylas.com"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {V3_API_KEY}',
    'Accept': 'application/json',
}


def create_grant():
    return requests.post(
        url=f"{DOMAIN}/v3/grants",
        headers=HEADERS,
        json={
            "provider": "virtual-calendar",
            "settings": {
                "email": "test-virtual-calendars@nylas.com"
            }
        },
    ).json()


def delete_grant(grant_id):
    return requests.delete(
        url=f"{DOMAIN}/v3/grants/{grant_id}",
        headers=HEADERS,
    ).json()


def create_calendar():
    return requests.post(
        url=f"{DOMAIN}/v3/grants/{grant_id}/calendars",
        headers=HEADERS,
        json={
            "name": "My New Calendar",
            "description": "Description of my new calendar",
            "location": "Location description",
            "timezone": "America/Los_Angeles"
        },
    ).json()

def delete_calendar(calendar_id):
    return requests.post(
        url=f"{DOMAIN}/v3/grants/{grant_id}/calendars/{calendar_id}",
        headers=HEADERS,
    ).json()


if __name__ == '__main__':
    """
    Requirement is to already have virtual calendar integration.
    """
    grant_id = None
    calendar_id = None

    try:
        # create grant
        res = create_grant()
        print(f"created grant: {res}")
        grant_id = res['data']['id']

        # create calendar
        res = create_calendar()
        print(f"created calendar: {res}")
        calendar_id = res['data']['id']

    finally:
        if calendar_id:
            res = delete_calendar(calendar_id)
            print(f"deleted calendar: {res}")
        if grant_id:
            res = delete_grant(grant_id)
            print(f"deleted grant: {res}")




    # create event
    # delete both

