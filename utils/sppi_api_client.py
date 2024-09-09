import os
import datetime

import requests
from utils.sppi_auth_client import SppiAuthClient
from dotenv import load_dotenv
from pydantic import BaseModel
from utils.pw_helpers import random_string

load_dotenv()

class SppiApiClient(SppiAuthClient):
    session: requests.Session
    base_url_api: str
    _url: str

    def __init__(self):
        self.session = requests.Session()
        self.base_url_api = os.getenv('RC_API_BASE_URL')
        self.base_url = os.getenv('BASE_URL_RC')
        self._secret_key = os.getenv('RC_API_SECRET_KEY')
        self._url = ''
        self._query = {}


    def bearer(self, token: str):
        self.session.headers.update({'Authorization': 'Bearer ' + token})

        return self

    def as_admin(self):
        tokens = self.get_access_refresh_token(os.getenv('RC_ADMIN_USER'), os.getenv('RC_ADMIN_PASSWORD'))
        access_token = tokens[0]
        self.bearer(access_token)

        return self

    def as_pilot(self):
        tokens = self.get_access_refresh_token(os.getenv('RC_PILOT_USER'), os.getenv('RC_PILOT_PASSWORD'))
        access_token = tokens[0]
        self.bearer(access_token)

        return self

    def as_atm_dispatcher_moscow(self):
        tokens = self.get_access_refresh_token(os.getenv('RC_ATM_DISPATCHER_MOSCOW_USER'), os.getenv('RC_ATM_DISPATCHER_MOSCOW_PASSWORD'))
        access_token = tokens[0]
        self.bearer(access_token)

        return self

    def admin_token(self):
        tokens = self.get_access_refresh_token(os.getenv('RC_ADMIN_USER'), os.getenv('RC_ADMIN_PASSWORD'))
        access_token = tokens[1]

        return access_token

    def pilot_token(self):
        tokens = self.get_access_refresh_token(os.getenv('RC_PILOT_USER'), os.getenv('RC_PILOT_PASSWORD'))
        access_token = tokens[1]

        return access_token

    def atm_dispatcher_moscow_token(self):
        tokens = self.get_access_refresh_token(os.getenv('RC_ATM_DISPATCHER_MOSCOW_USER'), os.getenv('RC_ATM_DISPATCHER_MOSCOW_PASSWORD'))
        access_token = tokens[1]

        return access_token

    def get(self, url: str = '', query=None):
        return self.session.get(self.base_url_api + self._url + str(url), params=query)

    def post(self, url: str = '', json=None, query=None):
        if json is None:
            json = {}
        return self.session.post(self.base_url_api + self._url + str(url), json=json, params=query)

    def patch(self, url: str = '', json=None, query=None):
        if json is None:
            json = {}
        return self.session.patch(self.base_url_api + self._url + str(url), json=json, params=query)

    def patch_disp(self, url: str = '', json=None, query=None):
        if json is None:
            json = {}
        return self.session.patch(self.base_url + self._url + str(url), json=json, params=query)

    def delete(self, url: str = ''):
        return self.session.delete(self.base_url_api + self._url + str(url), params=self._query)

    def shr(self):
        self._url = '/plans/shr'

        return self

    def shr_send(self, id):
        self._url = f'/plans/shr/{id}/send'

        return self

    def shr_cnl(self, id):
        self._url = f'/plans/shr/{id}/cnl'

        return self

    def shr_dep(self, id):
        self._url = f'/plans/shr/{id}/dep'

        return self

    def shr_arr(self, id):
        self._url = f'/plans/shr/{id}/arr'

        return self

    def shr_rej(self, id):
        self._url = f'/actm-service/shr/{id}/reject'

        return self

    def shr_ack(self, id):
        self._url = f'/actm-service/shr/{id}/approve'

        return self


    def get_created_shr_id_name(self):
        name = random_string() + 'Autotest'
        response = self.as_pilot().shr().post(json=
        {
            "name": f"{name}",
            "blank": {
        "field_7": "12345",
        "field_13": {
            "aerodrome": "UUDD",
            "time": "0800"
        },
        "field_15": {
            "level": {
                "value": "100",
                "unit": "mamsl"
            },
            "level_2": {
                "value": "100",
                "unit": "mamsl"
            },
            "geometry": {
                "type": "circle",
                "coordinates": "5524N03802E",
                "radius": 3
            }
        },
        "field_16": {
            "aerodrome": "UUDD",
            "total_eet": "0100"
        },
        "field_18": {
            "dof": int(datetime.datetime.now().timestamp()),
            "typ": "BLA"
        }
    },
            "atm_units": [
                {
                    "address": {
                        "type": "aftn",
                        "address": "UUWVZDZX"
                    },
                    "is_approving": True
                }
            ]
        }, query={'secret-key': self._secret_key}
        ).json()
        return response['id'], response['name']

    def send_created_shr(self, id):
        response = self.as_pilot().shr_send(id).post(json=
        {
            "atm_units": [
                {
                    "address": {
                        "type": "aftn",
                        "address": "UUWVZDZX"
                    },
                    "is_approving": True
                }
            ]
        }, query={'secret-key': self._secret_key, 'id': id}
        )


    def cnl_message_for_shr(self, id):
        response = self.as_pilot().shr_cnl(id).patch(query={'secret-key': self._secret_key, 'id': id}
        )

    def dep_message_for_shr(self, id):
        response = self.as_pilot().shr_dep(id).patch(
            json={
                "started_at": int(datetime.datetime.now().timestamp()),
                "start_place": "UUDD",
                "is_undefined_place": False
            },
            query={'secret-key': self._secret_key, 'id': id}
        )

    def arr_message_for_shr(self, id):
        response = self.as_pilot().shr_arr(id).patch(
            query={'secret-key': self._secret_key, 'id': id}
        )

    def rej_message_for_shr(self, id):
        response = self.as_atm_dispatcher_moscow().shr_rej(id).patch_disp(
            json={
  "processed_comment": "Не разрешаю"
}, query={'id': id}
        )
    def ack_message_for_shr(self, id):
        response = self.as_atm_dispatcher_moscow().shr_ack(id).patch_disp(
            json={
  "processed_comment": "Разрешаю"
}, query={'id': id}
        )