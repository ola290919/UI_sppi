import os
import time
from enum import Enum
from threading import Lock
from typing import Tuple

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class AuthTokensResult(BaseModel):
    access_token: str
    refresh_token: str


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str
    expiry_time: float


class SppiAuthClient:
    session: requests.Session
    _secret_key: str

    def __init__(self):
        self.session = requests.Session()
        self.base_url_api = os.getenv('RC_API_BASE_URL')
        self._secret_key = os.getenv('RC_API_SECRET_KEY')
        if not self._secret_key:
            raise Exception('SPPI_API_SECRET_KEY not set')


    def _make_tokens_request(self, login: str, password: str) -> AuthTokensResult:
        if not login or not password:
            raise Exception('Login and password are required for getting SPPI tokens')

        response = (self.session.post(self.base_url_api + '/auth/tokens',
                                      json={
                                          'login': login,
                                          'password': password
                                      },
                                      headers={
                                          'Content-Type': 'application/json',
                                          'secret-key': self._secret_key
                                      })
                    .json())

        AuthTokensResult.model_validate(response)

        return AuthTokensResult(**response)

    def _make_refresh_tokens_request(self, refresh_token: str) -> AuthTokensResult:
        response = (self.session.post(self.base_url_api + '/auth/tokens/refresh',
                                      json={
                                          'refresh_token': refresh_token,
                                      },
                                      headers={
                                          'Content-Type': 'application/json',
                                          'secret-key': self._secret_key
                                      })
                    .json())

        AuthTokensResult.model_validate(response)

        return AuthTokensResult(**response)

    def get_access_refresh_token(self, login: str, password: str) -> Tuple[str,str]:
        if not login or not password:
            raise Exception('Login and password are required for getting SPPI tokens')

        response = self._make_tokens_request(login, password)

        return response.access_token, response.refresh_token


    @staticmethod
    def get_auth_payload(login: str, password: str) -> Tuple[str, str]:
        url = f'{os.getenv('BASE_URL_RC')}/user-service/tokens'
        headers = {
            'captcha': 'skip-captcha',
            'skip-captcha': 'true'
        }
        data = {
            'login': login,
            'password': password
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data.get('access_payload') or not data.get('refresh_payload'):
            raise ValueError('No access or refresh payload in tokens response. Returned data: ' + json.dumps(data))

        return [data['access_payload'], data['refresh_payload']]

    def admin_tokens(self):

        return self.get_access_refresh_token(os.getenv('RC_ADMIN_USER'), os.getenv('RC_ADMIN_PASSWORD'))

    def pilot_tokens(self):
        return self.get_access_refresh_token(os.getenv('RC_PILOT_USER'), os.getenv('RC_PILOT_PASSWORD'))

    def atm_dispatcher_moscow_tokens(self):
        return self.get_access_refresh_token(os.getenv('RC_ATM_DISPATCHER_MOSCOW_USER'), os.getenv('RC_ATM_DISPATCHER_MOSCOW_PASSWORD'))


    def admin_payload(self):

        return self.get_auth_payload(os.getenv('RC_ADMIN_USER'), os.getenv('RC_ADMIN_PASSWORD'))

    def pilot_payload(self):

        return self.get_auth_payload(os.getenv('RC_PILOT_USER'), os.getenv('RC_PILOT_PASSWORD'))

    def atm_dispatcher_moscow_payload(self):

        return self.get_auth_payload(os.getenv('RC_ATM_DISPATCHER_MOSCOW_USER'), os.getenv('RC_ATM_DISPATCHER_MOSCOW_PASSWORD'))


auth = SppiAuthClient()


class As(Enum):
    ADMIN = 1
    PILOT = 2
    ATM_DISPATCHER_MOSCOW = 3

    def tokens(self):
        methods = {
            self.ADMIN: auth.admin_tokens,
            self.PILOT: auth.pilot_tokens,
            self.ATM_DISPATCHER_MOSCOW: auth.atm_dispatcher_moscow_tokens
        }

        return methods[self]()

    def payload(self):
        methods = {
            self.ADMIN: auth.admin_payload,
            self.PILOT: auth.pilot_payload,
            self.ATM_DISPATCHER_MOSCOW: auth.atm_dispatcher_moscow_payload
        }

        return methods[self]()
