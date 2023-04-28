from nylas import APIClient


if __name__ == '__main__':
    nylas = APIClient(
        CLIENT_ID,
        CLIENT_SECRET,
        ACCESS_TOKEN
    )

    # Create a new event
    event = nylas.events.create()

    event.title = "Party!"
    event.location = "My House!"
    event.description = "Let's celebrate our calendar integration!!"
    event.busy = True

    # Provide the appropriate id for a calendar to add the event to a specific calendar
    event.calendar_id = '<CALENDAR_ID>'

    # Participants are added as a list of dictionary objects
    # email is required, name is optional
    event.participants = [{"name": "My Nylas Friend", 'email': 'swag@nylas.com'}]

    # The event date/time can be set in one of 3 ways.
    event.when = {"start_time": 1577829600, "end_time": 1577840400}
    event.when = {"time": 1577829600}
    event.when = {"date": "2020-01-01"}
    event.when = {"start_date": "2019-08-29", "end_date": "2019-09-01"}

    # Configure recurring events using RRULE specifications
    event.recurrence = {"rrule": ["RRULE:FREQ=WEEKLY;BYDAY=MO"], "timezone": "America_Los_Angeles"}

    # .save()must be called to save the event to the third party provider
    # The event object must have values assigned to calendar_id and when before you can save it.
    event.save(notify_participants='true')
    # notify_participants='true' will send a notification email to
    # all email addresses specified in the participant subobject

    # Add conferencing details
    from nylas import APIClient

    nylas = APIClient(
        CLIENT_ID,
        CLIENT_SECRET,
        ACCESS_TOKEN
    )

    # Create a new event
    event = nylas.events.create()

    # add conferencing details
    event.conferencing = {
        "provider": "Zoom Meeting",
        "conferencing": {
            "autocreate": {
                "settings": {
                    "password": "1234",
                },
            },
        },
    }