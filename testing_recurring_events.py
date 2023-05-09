import time
from datetime import datetime

import requests
from nylas import APIClient
from client import CLIENT_ID
from client import CLIENT_SECRET
from client import ACCESS_TOKEN


def create_recurring_event(nylas: APIClient, calendar_id):
    # Create a new event
    event = nylas.events.create()
    event.title = "Test Recurring Event"

    event.calendar_id = calendar_id

    # The event date/time can be set in one of 3 ways.
    today_date = datetime.today().strftime('%Y-%m-%d')
    event.when = {"start_date": today_date, "end_date": today_date}

    # Configure recurring events using RRULE specifications
    # event.recurrence = {"rrule": ["RRULE:FREQ=DAILY;COUNT=3"], "timezone": "America_Los_Angeles"}
    event.save()
    # Create a new event
    return nylas.events.create()


def create_recurring_event_http(nylas: APIClient, calendar_id):
    today_date = datetime.today().strftime('%Y-%m-%d')
    url = "https://api.nylas.com/events"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "Test Recurring Event",
        "calendar_id": calendar_id,
        "when": {
            "start_date": today_date,
            "end_date": today_date
        },
        # "recurrence": {
        #     "rrule": [
        #         "RRULE:FREQ=WEEKLY;BYDAY=MO"
        #     ],
        #     "timezone": "America/New_York"
        # }
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    return response.json()


if __name__ == '__main__':
    nylas = APIClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=ACCESS_TOKEN
    )

    # getting primary calendar
    calendars = nylas.calendars.all()
    primary_calendar = None
    for calendar in calendars:
        if calendar['is_primary']:
            primary_calendar = calendar
    print(f"primary calendar ID: {primary_calendar['id']}")

    # creating recurring event
    recurring_event = create_recurring_event_http(nylas, primary_calendar['id'])
    print(f"recurring event ID: {recurring_event}")






