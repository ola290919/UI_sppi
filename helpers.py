import datetime
import json
import os
import random
import string

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


def random_string(lenght=10):
    return "".join([random.choice(string.ascii_letters) for _ in range(lenght)])


def category_up_to_0_15():
    return 'до 0,15 кг'


def category_from_0_15_up_to_30():
    return 'от 0,15 до 30 кг'


def category_more_than_30():
    return 'более 30 кг'


def level_unit_m_qne():
    return 'M/QNE'


def level_unit_m_amsl():
    return 'M/AMSL'


def flight_range_unit_m():
    return 'М'


def flight_range_unit_km():
    return 'КМ'


def flight_range_unit_nm():
    return 'NM'
