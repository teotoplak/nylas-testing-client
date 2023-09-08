import requests

from const import V3_API_KEY_STAGING
from const import V3_STAGING_DOMAIN


def create_redirect_uri():
    return requests.post(
        url=f"{V3_STAGING_DOMAIN}/v3/webhooks",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {V3_API_KEY_STAGING}',
            'Accept': 'application/json',
        },
        json={
          "description": "Teo test webhook destination",
          "trigger_types": [
            "calendar.created",
            "calendar.updated",
            "calendar.deleted",
            "event.created",
            "event.updated",
            "event.deleted",
          ],
          "callback_url": "https://uswest-staging-data-fetcher.nylas.com/webhooks-v3/",
          "notification_email_addresses": [
            "teo.toplak@nylas.com"
          ]
        }
    ).json()


if __name__ == '__main__':
    print(create_redirect_uri())