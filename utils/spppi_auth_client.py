import os
import time
import datetime
import json
from enum import Enum
from threading import Lock
from typing import Tuple
import datetime
import json
import os
from typing import TypedDict, List
from urllib.parse import urlparse

from playwright.sync_api import StorageState
from pydantic import BaseModel

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    jti: str
    login: str
    secret: str
    auth: TypedDict("Auth", {
        "protocol": str
    })
    iat: int
    exp: int
    iss: str

    @property
    def issued_at(self) -> datetime:
        return datetime.datetime.fromtimestamp(self.iat)

    @property
    def expires_at(self) -> datetime:
        return datetime.datetime.fromtimestamp(self.exp)


class TokensPayload(BaseModel):
    access_payload: TokenPayload
    refresh_payload: TokenPayload


class LocalStorage(BaseModel):
    name: str
    value: str


class Origin(BaseModel):
    origin: str
    localStorage: list[LocalStorage]


class Cookie(BaseModel):
    name: str
    value: str
    path: str
    domain: str
    httpOnly: bool
    secure: bool
    sameSite: str
    expires: int



class SpppiAuthClient:
    session: requests.Session
    _secret_key: str

    def __init__(self):
        self.session = requests.Session()
        self.base_url_api = os.getenv('RC_API_BASE_URL')
        self._base_url = os.getenv('BASE_URL_RC')
        self._secret_key = os.getenv('RC_API_SECRET_KEY')
        if not self._secret_key:
            raise Exception('SPPI_API_SECRET_KEY not set')


    def _make_auth_tokens_request(self, login: str, password: str) -> AuthTokens:
        response = (self.session.post(self.base_url_api + "auth/tokens",
                                      json={
                                          "login": login,
                                          "password": password
                                      },
                                      headers={
                                          "Content-Type": "application/json",
                                          "secret-key": self.secret_key
                                      }))

        response.raise_for_status()

        return AuthTokens.model_validate(response.json())

    def _make_auth_tokens_refresh_request(self, refresh_token: str) -> AuthTokens:
        response = (self.session.post(self.base_url_api + "auth/tokens/refresh",
                                      json={
                                          "refresh_token": refresh_token
                                      },
                                      headers={
                                          "Content-Type": "application/json",
                                          "secret-key": self.secret_key
                                      }))

        response.raise_for_status()

        return AuthTokens.model_validate(response.json())

    def get_tokens(self, login: str, password: str) -> AuthTokens:
        return self._make_auth_tokens_request(login, password)


    def _make_user_service_tokens_request(self, login: str, password: str) -> TokensPayload:
        response = (self.session.post(self._base_url + "user-service/tokens",
                                      json={
                                          "login": login,
                                          "password": password
                                      },
                                      headers={
                                          "Content-Type": "application/json",
                                          "captcha": "skip-captcha",
                                          "skip-captcha": "true"
                                      }))
        response.raise_for_status()

        return TokensPayload.model_validate(response.json())

    def _make_origins_data(self, tokens_payload: TokensPayload) -> Origin:
        return Origin.model_validate({
            "origin": self._base_url,
            "localStorage": [
                {
                    "name": "sppi6_client_auth",
                    "value": json.dumps({
                        "access_token_payload": dict(tokens_payload.access_payload),
                        "refresh_token_payload": dict(tokens_payload.refresh_payload),
                        "refresh_in_progress": False
                    })
                }
            ]
        })

    def _make_cookies(self, auth_tokens: AuthTokens) -> List[Cookie]:
        expires = int((datetime.datetime.now() + datetime.timedelta(
            minutes=os.getenv("SPPI_REFRESH_TOKEN_EXPIRE_MINUTES", 4))).timestamp())
        return [
            Cookie.model_validate({
                "name": "refresh_token",
                "value": auth_tokens.refresh_token,
                "path": "/",
                "domain": "." + urlparse(self._base_url).netloc.replace("www.", "").rstrip("/"),
                "httpOnly": True,
                "secure": False,
                "sameSite": "Strict",
                "expires": expires
            }),
            Cookie.model_validate({
                "name": "authorization",
                "value": auth_tokens.access_token,
                "path": "/",
                "domain": "." + urlparse(self._base_url).netloc.replace("www.", "").rstrip("/"),
                "httpOnly": True,
                "secure": False,
                "sameSite": "Strict",
                "expires": expires
            })
        ]

    def get_payload(self, login: str, password: str) -> TokensPayload:
        return self._make_user_service_tokens_request(login, password)

    def get_storage_state(self, login: str, password: str) -> StorageState:
        tokens_payload = self._make_user_service_tokens_request(login, password)
        auth_tokens = self.get_tokens(login, password)

        return StorageState(
            origins=[self._make_origins_data(tokens_payload).model_dump()],
            cookies=[cookie.model_dump() for cookie in self._make_cookies(auth_tokens)]
        )





#     def _make_tokens_request(self, login: str, password: str) -> AuthTokensResult:
#         if not login or not password:
#             raise Exception('Login and password are required for getting SPPI tokens')
#
#         response = (self.session.post(self.base_url_api + '/auth/tokens',
#                                       json={
#                                           'login': login,
#                                           'password': password
#                                       },
#                                       headers={
#                                           'Content-Type': 'application/json',
#                                           'secret-key': self._secret_key
#                                       })
#                     .json())
#
#         AuthTokensResult.model_validate(response)
#
#         return AuthTokensResult(**response)
#
#     def _make_refresh_tokens_request(self, refresh_token: str) -> AuthTokensResult:
#         response = (self.session.post(self.base_url_api + '/auth/tokens/refresh',
#                                       json={
#                                           'refresh_token': refresh_token,
#                                       },
#                                       headers={
#                                           'Content-Type': 'application/json',
#                                           'secret-key': self._secret_key
#                                       })
#                     .json())
#
#         AuthTokensResult.model_validate(response)
#
#         return AuthTokensResult(**response)
#
#     def get_access_refresh_token(self, login: str, password: str) -> Tuple[str,str]:
#         if not login or not password:
#             raise Exception('Login and password are required for getting SPPI tokens')
#
#         response = self._make_tokens_request(login, password)
#
#         return response.access_token, response.refresh_token
#
#
#     @staticmethod
#     def get_auth_payload(login: str, password: str) -> Tuple[str, str]:
#         url = f"{os.getenv('BASE_URL_RC')}/user-service/tokens"
#         headers = {
#             'captcha': 'skip-captcha',
#             'skip-captcha': 'true'
#         }
#         data = {
#             'login': login,
#             'password': password
#         }
#         response = requests.post(url, json=data, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         if not data.get('access_payload') or not data.get('refresh_payload'):
#             raise ValueError('No access or refresh payload in tokens response. Returned data: ' + json.dumps(data))
#
#         return [data['access_payload'], data['refresh_payload']]
#
#     def admin_tokens(self):
#
#         return self.get_access_refresh_token(os.getenv('RC_ADMIN_USER'), os.getenv('RC_ADMIN_PASSWORD'))
#
#     def pilot_tokens(self):
#         return self.get_access_refresh_token(os.getenv('RC_PILOT_USER'), os.getenv('RC_PILOT_PASSWORD'))
#
#     def atm_dispatcher_moscow_tokens(self):
#         return self.get_access_refresh_token(os.getenv('RC_ATM_DISPATCHER_MOSCOW_USER'), os.getenv('RC_ATM_DISPATCHER_MOSCOW_PASSWORD'))
#
#
#     def admin_payload(self):
#
#         return self.get_auth_payload(os.getenv('RC_ADMIN_USER'), os.getenv('RC_ADMIN_PASSWORD'))
#
#     def pilot_payload(self):
#
#         return self.get_auth_payload(os.getenv('RC_PILOT_USER'), os.getenv('RC_PILOT_PASSWORD'))
#
#     def atm_dispatcher_moscow_payload(self):
#
#         return self.get_auth_payload(os.getenv('RC_ATM_DISPATCHER_MOSCOW_USER'), os.getenv('RC_ATM_DISPATCHER_MOSCOW_PASSWORD'))
#
#     def make_storage_state_data(self, access_payload, refresh_payload):
#         data = {
#             "origin": os.getenv("BASE_URL_RC"),
#             "localStorage": [
#                 {
#                     "name": "sppi6_client_auth",
#                     "value": json.dumps({
#                         "access_token_payload": access_payload,
#                         "refresh_token_payload": refresh_payload,
#                         "refresh_in_progress": False
#                     })
#                 }
#             ]
#         }
#         return data
#
#     def make_cokies(self, access_token, refresh_token):
#         expires = int((datetime.datetime.now() + datetime.timedelta(minutes=3)).timestamp())
#         data = ([
#             {
#                 'name': 'refresh_token',
#                 'value': refresh_token,
#                 'path': '/',
#                 'domain': str(os.getenv("BASE_URL_RC")).replace('http://', '.'),
#                 'httpOnly': True,
#                 'secure': False,
#                 'sameSite': 'Strict',
#                 'expires': expires
#             },
#             {
#                 'name': 'authorization',
#                 'value': access_token,
#                 'path': '/',
#                 'domain': str(os.getenv("BASE_URL_RC")).replace('http://', '.'),
#                 'httpOnly': True,
#                 'secure': False,
#                 'sameSite': 'Strict',
#                 'expires': expires
#             }
#         ])
#         return data
#
#
#
#
#
#
# auth = SppiAuthClient()
#
#
# class As(Enum):
#     ADMIN = 1
#     PILOT = 2
#     ATM_DISPATCHER_MOSCOW = 3
#
#     def tokens(self):
#         methods = {
#             self.ADMIN: auth.admin_tokens,
#             self.PILOT: auth.pilot_tokens,
#             self.ATM_DISPATCHER_MOSCOW: auth.atm_dispatcher_moscow_tokens
#         }
#
#         return methods[self]()
#
#     def payload(self):
#         methods = {
#             self.ADMIN: auth.admin_payload,
#             self.PILOT: auth.pilot_payload,
#             self.ATM_DISPATCHER_MOSCOW: auth.atm_dispatcher_moscow_payload
#         }
#
#         return methods[self]()
