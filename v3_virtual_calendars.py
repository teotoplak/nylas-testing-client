from datetime import datetime
from datetime import timedelta

import requests
from const import V3_API_KEY_STAGING
from const import V3_API_KEY_PRODUCTION
from const import V3_LOCAL_PASSTHRU_DOMAIN
from const import V3_PROD_DOMAIN
from const import V3_STAGING_DOMAIN
from testing_recurring_events import exdate_format


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
    "name": "My New Calendar",
    "description": "Description of my new calendar",
    "location": "Location description",
    "timezone": "America/Los_Angeles",
    "metadata": METADATA,
}
tomorrow_date = (datetime.today() + timedelta(days=1)).strftime('%Y%m%d')
TEST_EVENT = {
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
    },
    "conferencing": {
        "provider": "Zoom Meeting",
        "details": {
            "url": "https://zoom.us/j/1234567890",
        }
    },
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


def create_event(url, event):
    return requests.post(
        url=f"{url}/events?calendar_id={calendar_id}",
        headers=HEADERS,
        json=event,
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
                'X-Nylas-Provider-Gma': 'virtual-calendar'
            }


        res = create_calendar(url)
        print(f"created calendar: {res}")
        if e2e:
            res = res['data']
        calendar_id = res['id']

        res = get_calendar(url, calendar_id)
        if e2e:
            res = res['data']
        print(f"get calendar: {res}")

        res = update_calendar(url, calendar_id)
        if e2e:
            res = res['data']
        print(f"update calendar: {res}")

        res = get_calendar(url, calendar_id)
        if e2e:
            res = res['data']
        print(f"get updated calendar: {res}")

        res = get_all_calendars(url, {
            "metadata_pair": "key1:foo",
        })
        print(f"get all calendars: {res}")
        if e2e:
            res = res['data']
        assert len(res) == 1

        res = create_event(url, TEST_EVENT)
        print(f"created event: {res}")
        if e2e:
            res = res['data']
        event_id = res['id']

        res = get_event(url, event_id)
        print(f"get event: {res}")
        if e2e:
            res = res['data']

        res = get_all_events(url, {
            "expand_recurring": "true",
        })
        if e2e:
            res = res['data']
        new_child_event = res[0]
        # must add this because of bug in VCs not storing recurrence.timezone
        new_child_event['recurrence']['timezone'] = 'UTC'
        new_child_event['title'] = 'Updated Child Title'
        new_child_event['participants'][0] = {
            "name": "Aristotle",
            "email": "aristotle@nylas.com",
            "status": "no"
        }
        new_child_event['metadata'] = METADATA_NEW
        # otherwise request will be rejected since you can't send event.when.object
        del new_child_event['when']['object']
        res = update_event(url, calendar_id, new_child_event['id'], new_child_event)
        print(f"updated event: {res}")
        if e2e:
            res = res['data']
        assert res['participants'][0]['status'] == 'no'
        print(f"updated child event: {res}")

        res = get_event(url, res['id'])
        if e2e:
            res = res['data']
        print(f"get updated child event: {res}")

        res = get_event(url, event_id)
        if e2e:
            res = res['data']
        new_event = res
        new_event['title'] = 'Updated Title'
        new_event['participants'][0] = {
            "name": "Aristotle",
            "email": "aristotle@nylas.com",
            "status": "no"
        }
        new_event['metadata'] = METADATA_NEW
        # must add this because of bug in VCs not storing recurrence.timezone
        new_event['recurrence']['timezone'] = 'UTC'
        # otherwise request will be rejected since you can't send event.when.object
        del new_event['when']['object']
        res = update_event(url, calendar_id, event_id, new_event)
        print(f"updated event: {res}")
        if e2e:
            res = res['data']
        assert res['participants'][0]['status'] == 'no'

        res = get_event(url, event_id)
        if e2e:
            res = res['data']
        print(f"get updated event: {res}")

        res_none = get_event(url, "non-existent-event-id")
        print(f"for getting non-existent event: {res_none}")

        res = get_all_events(url, {
            "expand_recurring": "true",
        })
        print(f"get all events: {res}")
        if e2e:
            res = res['data']
        print(f"get all events count: {len(res)}")

        res = get_all_events(url, {
            "metadata_pair": "key1:foo",
        })
        print(f"get all events with metadata filter: {res}")
        if e2e:
            res = res['data']
        # assert len(res) == 1

    finally:
        print(f"=== CLEANING UP ===")
        if event_id:
            res = delete_event(url, event_id)
            print(f"deleted event: {res}")
        if calendar_id:
            res = delete_calendar(url, calendar_id)
            print(f"deleted calendar: {res}")
        if e2e and grant_id:
            res = delete_grant(grant_id)
            print(f"deleted grant: {res}")

