from datetime import datetime
from datetime import timedelta
import time
import requests
from const import V3_API_KEY_STAGING
from const import V3_API_KEY_PRODUCTION
from const import V3_LOCAL_PASSTHRU_DOMAIN
from const import V3_PROD_DOMAIN
from const import V3_STAGING_DOMAIN


METADATA = {
    "key1": "foo",
    "key-to-persist": "initial-value",
    "key-to-delete": "initial-value",
}
METADATA_NEW = {
    "key1": "foo",
    "key-to-persist": "updated-value",
}
TEST_CALENDAR = {
    "name": "My New Calendar - Performance Testing",
    "description": "Test calendar for performance testing",
}
LOCAL_TESTING_GRANT = "local_testing_grant"


def create_event(date):
    return {
        "title": "Performance Testing Event",
        "when": {
          "date": date,
        },
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=3",
        ],
        "metadata": METADATA
    }


def create_grant(host_url):
    return requests.post(
        url=f"{host_url}/v3/grants",
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
        url=f"{V3_STAGING_DOMAIN}/v3/grants/{grant_id}",
        headers=HEADERS,
    ).json()


def create_calendar(url):
    return requests.post(
        url=f"{url}/calendars",
        headers=HEADERS,
        json=TEST_CALENDAR,
    ).json()


def update_calendar(url, calendar_id):
    new_calendar = TEST_CALENDAR
    new_calendar['name'] = 'Updated Name'
    new_calendar['metadata'] = METADATA_NEW
    return requests.put(
        url=f"{url}/calendars/{calendar_id}",
        headers=HEADERS,
        json=TEST_CALENDAR,
    ).json()


def get_calendar(url, calendar_id):
    return requests.get(
        url=f"{url}/calendars/{calendar_id}",
        headers=HEADERS,
    ).json()


def get_all_calendars(url, params):
    return requests.get(
        url=f"{url}/calendars",
        params=params,
        headers=HEADERS,
    ).json()


def create_event_with_url(url, event_date):
    return requests.post(
        url=f"{url}/events?calendar_id={calendar_id}",
        headers=HEADERS,
        json=create_event(event_date),
    ).json()


def update_event(url, calendar_id, event_id, new_event):
    return requests.put(
        url=f"{url}/events/{event_id}?calendar_id={calendar_id}",
        headers=HEADERS,
        json=new_event,
    ).json()


def get_all_events(url, params):
    return requests.get(
        url=f"{url}/events?calendar_id={calendar_id}",
        params=params,
        headers=HEADERS,
    ).json()


def get_event(url, event_id):
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
    # host = "prod"
    # host = "local"
    url = None

    e2e = (host == "staging") or (host == "prod")

    try:
        if host == "staging":
            HEADERS = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {V3_API_KEY_STAGING}',
                'Accept': 'application/json',
                'X-Nylas-Provider-Gma': 'virtual-calendar'
            }
            res = create_grant(V3_STAGING_DOMAIN)
            print(f"created grant: {res}")
            grant_id = res['data']['id']
            url = f"{V3_STAGING_DOMAIN}/v3/grants/{grant_id}"
        if host == "prod":
            HEADERS = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {V3_API_KEY_PRODUCTION}',
                'Accept': 'application/json',
                'X-Nylas-Provider-Gma': 'virtual-calendar'
            }
            res = create_grant(V3_PROD_DOMAIN)
            print(f"created grant: {res}")
            grant_id = res['data']['id']
            url = f"{V3_PROD_DOMAIN}/v3/grants/{grant_id}"
        if host == "local":
            url = f"{V3_LOCAL_PASSTHRU_DOMAIN}/v3"
            HEADERS = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Nylas-Provider-Gma': 'virtual-calendar',
                'X-Nylas-Grant-Id': f'{LOCAL_TESTING_GRANT}'
            }

        res = create_calendar(url)
        print(f"created calendar: {res}")
        res = res['data']
        calendar_id = res['id']

        for i in range(0, 5):
            date = datetime.today().strftime('%Y%m%d')
            res = create_event_with_url(url, date)
            print(f"created event: {res} with date: {date}")

        print(f"=== GET ALL EVENTS ===")
        measure_start_time = time.time()
        res = get_all_events(url, {
            "expand_recurring": "true",
            # start and end time querying for one week in timestamps
            "start": int(datetime.today().timestamp()),
            "end": int((datetime.today() + timedelta(days=1)).timestamp()),
        })
        print(f"get all events: {res}")
        res = res['data']
        print(f"get all events count: {len(res)}")
        print(f"get all events took: {time.time() - measure_start_time}")

    finally:
        print(f"=== CLEANING UP ===")
        if calendar_id:
            res = delete_calendar(url, calendar_id)
            print(f"deleted calendar: {res}")
        if e2e and grant_id:
            res = delete_grant(grant_id)
            print(f"deleted grant: {res}")

