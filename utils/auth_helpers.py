import datetime
import json
import os

from dotenv import load_dotenv

load_dotenv()


def make_storage_state_data(access_payload, refresh_payload):
    data = {
        "origin": os.getenv("BASE_URL_RC"),
        "localStorage": [
            {
                "name": "sppi6_client_auth",
                "value": json.dumps({
                    "access_token_payload": access_payload,
                    "refresh_token_payload": refresh_payload,
                    "refresh_in_progress": False
                })
            }
        ]
    }
    return data


def make_cokies(access_token, refresh_token):
    expires = int((datetime.datetime.now() + datetime.timedelta(minutes=3)).timestamp())
    data = ([
        {
            'name': 'refresh_token',
            'value': refresh_token,
            'path': '/',
            'domain': str(os.getenv("BASE_URL_RC")).replace('http://', '.'),
            'httpOnly': True,
            'secure': False,
            'sameSite': 'Strict',
            'expires': expires
        },
        {
            'name': 'authorization',
            'value': access_token,
            'path': '/',
            'domain': str(os.getenv("BASE_URL_RC")).replace('http://', '.'),
            'httpOnly': True,
            'secure': False,
            'sameSite': 'Strict',
            'expires': expires
        }
    ])
    return data
