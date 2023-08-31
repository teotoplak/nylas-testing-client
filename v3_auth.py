import requests


def create_grant(host_url, headers):
    return requests.post(
        url=f"{host_url}/v3/grants",
        headers=headers,
        json={
            "provider": "virtual-calendar",
            "settings": {
                "email": "test-virtual-calendars@nylas.com"
            }
        },
    ).json()

