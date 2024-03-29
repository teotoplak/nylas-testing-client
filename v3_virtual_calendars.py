from datetime import datetime
from datetime import timedelta

import requests
from const import V3_API_KEY_STAGING
from const import V3_API_KEY_PRODUCTION
from const import V3_LOCAL_PASSTHRU_DOMAIN
from const import V3_PROD_DOMAIN
from const import V3_STAGING_DOMAIN
from testing_recurring_events import exdate_format
from v3_auth import create_grant

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
tomorrow_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
tomorrow_date_short = (datetime.today() + timedelta(days=1)).strftime('%Y%m%d')
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
    "recurrence": [
        "RRULE:FREQ=WEEKLY;COUNT=3",
        exdate_format([tomorrow_date_short])
  ],
    "conferencing": {
        "provider": "Google Meet",
        "details": {
            "url": "https://zoom.us/j/1234567890",
            "phone": ["+1 123 456 7890", "+1 123 456 7891"],
        }
    },
    "metadata": METADATA
}

TMP_CHILD_TEST_EVENT = {
    "description": "",
    "hide_participants": False,
    # "participants": [],
    "reminders": {
      "use_default": True,
      "overrides": None
    },
    "title": "recurring test 12/6/23",
    "when": {
        "start_time": 1703025000,
        "start_timezone": "America/New_York",
        "end_time": 1703028600,
        "end_timezone": "America/New_York"
    },
    "conferencing": {
        "provider": "Google Meet",
        "details": {
            "url": "https://zoom.us/j/1234567890",
            "phone": ["+1 123 456 7890", "+1 123 456 7891"],
        }
    },
}


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

    # host = "staging"
    host = "prod"
    # host = "local"
    url = None

    try:

        if host == "staging":
            HEADERS = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {V3_API_KEY_STAGING}',
                'Accept': 'application/json',
                'X-Nylas-Provider-Gma': 'virtual-calendar'
            }
            res = create_grant(V3_STAGING_DOMAIN, HEADERS)
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
            res = create_grant(V3_PROD_DOMAIN, HEADERS)
            print(f"created grant: {res}")
            grant_id = res['data']['id']
            url = f"{V3_PROD_DOMAIN}/v3/grants/{grant_id}"
        if host == "local":
            url = f"{V3_LOCAL_PASSTHRU_DOMAIN}/v3"
            HEADERS = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Nylas-Provider-Gma': 'virtual-calendar',
                'X-Nylas-Grant-Id': 'test-grant-id',
            }


        res = create_calendar(url)
        print(f"created calendar: {res}")
        res = res['data']
        calendar_id = res['id']

        res = get_calendar(url, calendar_id)
        print(f"get calendar: {res}")
        res = res['data']

        res = update_calendar(url, calendar_id)
        print(f"update calendar: {res}")
        res = res['data']

        res = get_calendar(url, calendar_id)
        print(f"get updated calendar: {res}")
        res = res['data']

        res = get_all_calendars(url, {
            "metadata_pair": "key1:foo",
        })
        print(f"get all calendars: {res}")
        res = res['data']
        # assert len(res) == 1

        res = create_event(url, TEST_EVENT)
        print(f"created event: {res}")
        res = res['data']
        event_id = res['id']

        res = get_event(url, event_id)
        print(f"get event: {res}")
        res = res['data']

        res = get_all_events(url, {
            "expand_recurring": "true",
        })
        res = res['data']
        new_child_event = res[0]
        new_child_event['title'] = 'Updated Child Title'
        new_child_event['participants'][0] = {
            "name": "Aristotle",
            "email": "aristotle@nylas.com",
            "status": "no"
        }
        new_child_event['metadata'] = METADATA_NEW
        # otherwise request will be rejected since you can't send event.when.object
        del new_child_event['when']['object']
        del new_child_event['organizer']
        idchild = new_child_event['id']
        del new_child_event['id']
        res = update_event(url, calendar_id, idchild, new_child_event)
        print(f"updated child event: {res}")
        res = res['data']
        # assert res['participants'][0]['status'] == 'no'
        res = get_event(url, res['id'])
        print(f"get updated child event: {res}")
        res = res['data']


        # updating event (not a child one)
        res = get_event(url, event_id)
        res = res['data']
        new_event = res
        new_event['title'] = 'Updated Title'
        new_event['participants'][0] = {
            "name": "Aristotle",
            "email": "aristotle@nylas.com",
            "status": "no"
        }
        new_event['metadata'] = METADATA_NEW
        # otherwise request will be rejected since you can't send event.when.object
        del new_event['when']['object']
        # organiser is not a modifiable field.
        del new_event['organizer']
        del new_event['id']
        res = update_event(url, calendar_id, event_id, new_event)
        print(f"updated event: {res}")
        res = res['data']
        assert res['participants'][0]['status'] == 'no'

        res = get_event(url, event_id)
        res = res['data']
        print(f"get updated event: {res}")

        res_none = get_event(url, "non-existent-event-id")
        print(f"for getting non-existent event: {res_none}")

        res = get_all_events(url, {
            "expand_recurring": "true",
        })
        print(f"get all events: {res}")
        res = res['data']
        print(f"get all events count: {len(res)}")

        res = get_all_events(url, {
            "metadata_pair": "key1:foo",
        })
        print(f"get all events with metadata filter: {res}")
        res = res['data']
        # assert len(res) == 1

    except Exception as e:
        print(f"=== ERROR ===")
        print(e)
    finally:
        print(f"=== CLEANING UP ===")
        if event_id:
            res = delete_event(url, event_id)
            print(f"deleted event: {res}")
        # WE CANNOT DELETE PRIMARY CALENDAR ANYMORE; WE ARE JUST LEAVING THIS DUMMY DATA IN THE SYSTEM.
        # if calendar_id:
        #     res = delete_calendar(url, calendar_id)
        #     print(f"deleted calendar: {res}")
        if grant_id:
            res = delete_grant(grant_id)
            print(f"deleted grant: {res}")

