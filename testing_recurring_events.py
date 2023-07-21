import time
from datetime import datetime
from datetime import timedelta

import requests
from nylas import APIClient
from const import V2_CLIENT_ID
from const import V2_CLIENT_SECRET
from const import V2_ACCESS_TOKEN


def get_event(calendar_id, event_id, expanded):
    url = "https://api.nylas.com/events"
    params = {
        "calendar_id": calendar_id,
        "event_id": event_id,
        "expand_recurring": expanded
    }
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {V2_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_events(calendar_id, starts_after, ends_before):
    url = "https://api.nylas.com/events"
    params = {
        "calendar_id": calendar_id,
        "starts_after": starts_after,
        "ends_before": ends_before,
        "expand_recurring": False
    }
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {V2_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()



def update_event(event_id):
    url = f"https://api.nylas.com/events/{event_id}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {V2_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "Test Recurring Event Updated",
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()


def create_recurring_event_http(nylas: APIClient, calendar_id):
    today_date = datetime.today().strftime('%Y-%m-%d')
    today_date_short = datetime.today().strftime('%Y%m%d')
    tomorrow_date_short = (datetime.today() + timedelta(days=1)).strftime('%Y%m%d')
    url = "https://api.nylas.com/events"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {V2_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "Test Recurring Event",
        "calendar_id": calendar_id,
        "when": {
            "start_date": today_date,
            "end_date": today_date
        },
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=4",
            exdate_format([today_date_short, tomorrow_date_short]),
        ],
        "metadata": {
            "recurring_test": "yes"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def exdate_format(dates):
    dates_formatted = ""
    for date in dates:
        dates_formatted += f"{date},"
    return f"EXDATE:{dates_formatted[:-1]}"


if __name__ == '__main__':
    nylas = APIClient(
        client_id=V2_CLIENT_ID,
        client_secret=V2_CLIENT_SECRET,
        access_token=V2_ACCESS_TOKEN
    )

    # getting primary calendar
    calendars = nylas.calendars.all()
    primary_calendar = None
    for calendar in calendars:
        if calendar['is_primary']:
            primary_calendar = calendar
    print(f"primary calendar ID: {primary_calendar['id']}")

    recurring_event_id = None

    try:
        # creating recurring event
        recurring_event = create_recurring_event_http(nylas, primary_calendar['id'])
        print(f"recurring event created ID: {recurring_event}")
        recurring_event_id = recurring_event['id']

        expanded_recurring_event = get_event(primary_calendar['id'], recurring_event_id, "true")
        print(f"expanded recurring event: {expanded_recurring_event}")

        # updating child of recurring event
        updated_event = update_event(expanded_recurring_event[0]['id'])
        print(f"updated child event ID: {updated_event}")

        expanded_recurring_event_after_update = get_event(primary_calendar['id'], recurring_event_id, "true")
        print(f"expanded recurring event: {expanded_recurring_event_after_update}")

        recurring_event_after_update = get_event(primary_calendar['id'], recurring_event_id, "false")
        print(f"recurring event: {recurring_event_after_update}")

        # to see if we treat updated child event as a separate event
        all_events = get_events(
            primary_calendar['id'],
            datetime.now().timestamp() - timedelta(days=1).total_seconds(),
            datetime.now().timestamp() + timedelta(weeks=1).total_seconds()
        )
        print(f"all events: {all_events}")

    finally:
        if recurring_event_id:
            nylas.events.delete(recurring_event_id)
            print(f"recurring event deleted ID: {recurring_event_id}")






