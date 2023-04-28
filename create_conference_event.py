
from client import nylas

CALENDAR_ID = "c95el2sjcmudyo39jwp3rnr83"
PARTICIPANTS = [
        {
            "name": "Teo",
            'email': 'teotoplak95@gmail.com'
        },
        {
            "name": "Nexpi director",
            'email': 'nexpi.info@gmail.com'
        },
    ]

if __name__ == '__main__':

    # Create a new event
    event = nylas.events.create()

    event.title = "Party!"
    event.location = "My House!"
    event.description = "Let's celebrate our calendar integration!!"
    event.busy = True

    # Provide the appropriate id for a calendar to add the event to a specific calendar
    event.calendar_id = CALENDAR_ID

    # Participants are added as a list of dictionary objects
    # email is required, name is optional
    event.participants = PARTICIPANTS

    # The event date/time can be set in one of 3 ways.
    event.when = {"start_date": "2023-04-28", "end_date": "2023-04-29"}

    # Configure recurring events using RRULE specifications
    # event.recurrence = {"rrule": ["RRULE:FREQ=WEEKLY;BYDAY=MO"], "timezone": "America_Los_Angeles"}

    # .save()must be called to save the event to the third party provider
    # The event object must have values assigned to calendar_id and when before you can save it.
    event.save(notify_participants='true')
    # notify_participants='true' will send a notification email to
    # all email addresses specified in the participant subobject

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