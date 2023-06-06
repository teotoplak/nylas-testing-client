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
            "timezone": "America/Los_Angeles",
            "metadata": {
                "foo": "bar"
            }
        },
    ).json()


def create_event():
    return requests.post(
        url=f"{DOMAIN}/v3/grants/{grant_id}/events?calendar_id={calendar_id}",
        headers=HEADERS,
        json={
            "title": "Birthday Party",
            "status": "confirmed",
            "busy": True,
            "participants": [
              {
                "name": "Aristotle",
                "email": "aristotle@nylas.com",
                "status": "yes"
              }
            ],
            "description": "Come ready to skate",
            "when": {
              "time": 1408875644
            },
            "location": "Roller Rink",
            "recurrence": {
              "rrule": [
                "RRULE:FREQ=WEEKLY;COUNT=8"
              ],
              "timezone": "America/New_York"
            }
        },
    ).json()


def get_event():
    return requests.get(
        url=f"{DOMAIN}/v3/grants/{grant_id}/events/{event_id}?calendar_id={calendar_id}",
        headers=HEADERS,
    ).json()


def delete_calendar(calendar_id):
    return requests.delete(
        url=f"{DOMAIN}/v3/grants/{grant_id}/calendars/{calendar_id}",
        headers=HEADERS,
    ).json()


def delete_event(event_id):
    return requests.delete(
        url=f"{DOMAIN}/v3/grants/{grant_id}/events/{event_id}?calendar_id={calendar_id}",
        headers=HEADERS,
    ).json()


if __name__ == '__main__':
    """
    Requirement is to already have virtual calendar integration.
    """
    grant_id = None
    calendar_id = None
    event_id = None

    try:
        res = create_grant()
        print(f"created grant: {res}")
        grant_id = res['data']['id']

        res = create_calendar()
        print(f"created calendar: {res}")
        calendar_id = res['data']['id']

        res = create_event()
        print(f"created event: {res}")
        event_id = res['data']['id']

        res = get_event()
        print(f"get event: {res}")

    finally:
        if event_id:
            res = delete_event(event_id)
            print(f"deleted event: {res}")
        if calendar_id:
            res = delete_calendar(calendar_id)
            print(f"deleted calendar: {res}")
        if grant_id:
            res = delete_grant(grant_id)
            print(f"deleted grant: {res}")

