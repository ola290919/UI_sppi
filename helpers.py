import datetime
import json
import os
import random
import string
from enum import Enum

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


class Weight:

    def up_to_0_15():
        return 'до 0,15 кг'

    def from_0_15_up_to_30():
        return 'от 0,15 до 30 кг'

    def more_than_30():
        return 'более 30 кг'


class Unit:
    def m_qne():
        return 'M/QNE'

    def m_amsl():
        return 'M/AMSL'

    def fl():
        return 'FL'

    def ft_agl():
        return 'FT/AGL'

    def tabel():
        return 'ТАБЕЛЬ'

    def m():
        return 'М'

    def km():
        return 'КМ'

    def nm():
        return 'NM'

class FlightRules:
    def i():
        return 'I ППП'

    def v():
        return 'V ПВП'

    def y():
        return 'Y ППП/ПВП'

    def z():
        return 'Z ПВП/ППП'

class FlightType:
    def s():
        return 'S по расписанию'

    def n():
        return 'N вне расписания'

    def g():
        return 'G АОН'

    def m():
        return 'M гос. авиация'

    def x():
        return 'X прочее'

class TurbulenceCat:
    def h():
        return 'H от 136000 до 500000 кг'

    def j():
        return 'J A-380-800'

    def m():
        return 'M от 7000 до 136000 кг'

    def l():
        return 'L до 7000 кг'

class FplType:
    def vs_flight():
        return 'Полёт воздушного судна'

    def utp_ad():
        return 'УТП в районе аэродрома'

    def utp_area():
        return 'УТП с площадок'
