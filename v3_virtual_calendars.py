from datetime import datetime
from datetime import timedelta

import requests
from client import V3_API_KEY
from testing_recurring_events import exdate_format

STAGING_HOST = "https://api-staging.us.nylas.com"
LOCAL_PASSTHRU_DOMAIN = "http://localhost:8008"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {V3_API_KEY}',
    'Accept': 'application/json',
    'X-Nylas-Provider-Gma': 'virtual-calendar'
}


def create_grant():
    return requests.post(
        url=f"{STAGING_HOST}/v3/grants",
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
        url=f"{STAGING_HOST}/v3/grants/{grant_id}",
        headers=HEADERS,
    ).json()


def create_calendar(url):
    return requests.post(
        url=f"{url}/calendars",
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


def create_event(url):
    tomorrow_date = (datetime.today() + timedelta(days=1)).strftime('%Y%m%d')
    return requests.post(
        url=f"{url}/events?calendar_id={calendar_id}",
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
              "date": tomorrow_date,
                # "time": 1408875644
            },
            "location": "Roller Rink",
            "recurrence": {
              "rrule": [
                "RRULE:FREQ=WEEKLY;COUNT=3",
                exdate_format([tomorrow_date])
              ],
              "timezone": "America/New_York"
            }
        },
    ).json()


def get_all_events(url, params):
    return requests.get(
        url=f"{url}/events?calendar_id={calendar_id}",
        params=params,
        headers=HEADERS,
    ).json()


def get_event(url):
    return requests.get(
        url=f"{url}/events/{event_id}?calendar_id={calendar_id}",
        headers=HEADERS,
    ).json()


def delete_calendar(url, calendar_id):
    return requests.delete(
        url=f"{url}/calendars/{calendar_id}",
        headers=HEADERS,
    ).json()


def delete_event(url, event_id):
    return requests.delete(
        url=f"{url}/events/{event_id}?calendar_id={calendar_id}",
        headers=HEADERS,
    ).json()


if __name__ == '__main__':
    """
    Requirement is to already have virtual calendar integration.
    """
    grant_id = None
    calendar_id = None
    event_id = None

    host = "staging"
    # host = "passthru"
    url = None

    try:

        if host == "staging":
            res = create_grant()
            print(f"created grant: {res}")
            grant_id = res['data']['id']
            url = f"{STAGING_HOST}/v3/grants/{grant_id}"
        if host == "passthru":
            url = f"{LOCAL_PASSTHRU_DOMAIN}/v3"

        res = create_calendar(url)
        print(f"created calendar: {res}")
        if host == "staging":
            res = res['data']
        calendar_id = res['id']

        res = create_event(url)
        print(f"created event: {res}")
        if host == "staging":
            res = res['data']
        event_id = res['id']

        res = get_event(url)
        if host == "staging":
            res = res['data']
        print(f"get event: {res}")

        res = get_all_events(url, {
            "expand_recurring": "true",
        })
        if host == "staging":
            res = res['data']
        print(f"get all events: {res}")
        print(f"get all events count: {len(res)}")

    finally:
        if event_id:
            res = delete_event(url, event_id)
            print(f"deleted event: {res}")
        if calendar_id:
            res = delete_calendar(url, calendar_id)
            print(f"deleted calendar: {res}")
        if host == "staging" and grant_id:
            res = delete_grant(grant_id)
            print(f"deleted grant: {res}")

