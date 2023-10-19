import requests

import v3_auth
from const import V3_API_KEY_PRODUCTION
from const import V3_API_KEY_STAGING
from const import V3_CLIENT_ID_PRODUCTION
from const import V3_CLIENT_ID_STAGING
from const import V3_PROD_DOMAIN
from const import V3_STAGING_DOMAIN


def get_app():
    return requests.get(
        url=f"{V3_STAGING_DOMAIN}/v3/applications",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {V3_API_KEY_STAGING}',
            'Accept': 'application/json',
        },
    ).json()


def list_google_grants():
    return requests.get(
        url=f"{V3_STAGING_DOMAIN}/v3/grants",
        params={
            "provider": "google",
        },
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {V3_API_KEY_STAGING}',
            'Accept': 'application/json',
        },
    ).json()


def create_redirect_uri():
    return requests.post(
        url=f"{V3_STAGING_DOMAIN}/v3/applications/redirect-uris",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {V3_API_KEY_STAGING}',
            'Accept': 'application/json',
        },
        json={
          "url": "https://api-staging.us.nylas.com/v3/connect/callback",
          "platform": "web",
        }
    ).json()


def get_auth_url():
    return requests.post(
        url=f"{V3_STAGING_DOMAIN}/v3/connect/auth",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {V3_API_KEY_STAGING}',
            'Accept': 'application/json',
        },
        json={
            "client_id": V3_CLIENT_ID_STAGING,
            "redirect_uri": "https://api-staging.us.nylas.com/v3/connect/callback",
            "response_type": "code",
            "provider": "google",
        }
    ).json()

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {V3_API_KEY_STAGING}',
    'Accept': 'application/json',
    'X-Nylas-Provider-Gma': 'google'
}

# def create_grant(host_url):
#     return requests.post(
#         url=f"{host_url}/v3/grants",
#         headers=HEADERS,
#         json={
#             "provider": "google",
#             "settings": {
#                 "email": "test-virtual-calendars@nylas.com"
#                 "refresh_token": "1//0gY5CZ4Z3QqZUCgYIAR",
#             }
#         },
#     ).json()


def delete_grant(grant_id):
    return requests.delete(
        url=f"{V3_STAGING_DOMAIN}/v3/grants/{grant_id}",
        headers=HEADERS,
    ).json()


if __name__ == '__main__':
    # print(get_app())
    # print(create_redirect_uri())
    # print(get_auth_url())
    print(list_google_grants())
    grant_id = None
    try:
        # grant_id = create_grant(V3_STAGING_DOMAIN)
        print(grant_id)
    finally:
        if grant_id:
            delete_grant(grant_id)


