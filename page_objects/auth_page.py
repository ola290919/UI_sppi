import os
import time
from enum import Enum
from threading import Lock

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


class AuthPage:
    session: requests.Session
    _base_url: str
    _instance = None
    _lock = Lock()
    _secret_key: str
    tokens: {AuthToken}
    stend: str

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AuthPage, cls).__new__(cls)
                cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.session = requests.Session()
            self._initialized = True
            self._base_url = os.getenv('RC_API_BASE_URL')
            self.secret_key = os.getenv('RC_API_SECRET_KEY')
            if not self.secret_key:
                raise Exception('SPPI_API_SECRET_KEY not set')
            self.tokens = {}

    def _make_tokens_request(self, login: str, password: str) -> AuthTokensResult:
        if not login or not password:
            raise Exception('Login and password are required for getting SPPI tokens')

        response = (self.session.post(self._base_url + '/auth/tokens',
                                      json={
                                          'login': login,
                                          'password': password
                                      },
                                      headers={
                                          'Content-Type': 'application/json',
                                          'secret-key': self.secret_key
                                      })
                    .json())

        AuthTokensResult.model_validate(response)

        return AuthTokensResult(**response)

    def _make_refresh_tokens_request(self, refresh_token: str) -> AuthTokensResult:
        response = (self.session.post(self._base_url + '/auth/tokens/refresh',
                                      json={
                                          'refresh_token': refresh_token,
                                      },
                                      headers={
                                          'Content-Type': 'application/json',
                                          'secret-key': self.secret_key
                                      })
                    .json())

        AuthTokensResult.model_validate(response)

        return AuthTokensResult(**response)

    def get_access_refresh_token(self, login: str, password: str) -> str:
        if not login or not password:
            raise Exception('Login and password are required for getting SPPI tokens')

        # Check if token already exists
        if login in self.tokens:
            current_time = time.time()
            token_data = self.tokens[login]
            # Check if token is not expired
            if current_time < token_data['expiry_time']:
                return token_data['access_token']
            else:
                # Refresh token
                response = self._make_refresh_tokens_request(token_data['refresh_token'])

                self.tokens[login] = {
                    'access_token': response.access_token,
                    'refresh_token': response.refresh_token,
                    'expiry_time': time.time() + float(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')) * 60
                }

                return self.tokens[login]['access_token']

        # Create new token
        response = self._make_tokens_request(login, password)

        self.tokens[login] = {
            'access_token': response.access_token,
            'refresh_token': response.refresh_token,
            'expiry_time': time.time() + float(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')) * 60
        }

        return (self.tokens[login]['access_token'], self.tokens[login]['refresh_token'])

    def admin_tokens(self):

        return self.get_access_refresh_token(os.getenv('RC_ADMIN_USER'), os.getenv('RC_ADMIN_PASSWORD'))

    def pilot_tokens(self):
        return self.get_access_refresh_token(os.getenv('RC_PILOT_USER'), os.getenv('RC_PILOT_PASSWORD'))

    @staticmethod
    def get_auth_payload(login: str, password: str):
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

    def admin_payload(self):

        return self.get_auth_payload(os.getenv('RC_ADMIN_USER'), os.getenv('RC_ADMIN_PASSWORD'))

    def pilot_payload(self):

        return self.get_auth_payload(os.getenv('RC_PILOT_USER'), os.getenv('RC_PILOT_PASSWORD'))


auth = AuthPage()


class As(Enum):
    ADMIN = 1
    PILOT = 2

    def tokens(self):
        methods = {
            self.ADMIN: auth.admin_tokens,
            self.PILOT: auth.pilot_tokens
        }

        return methods[self]()

    def payload(self):
        methods = {
            self.ADMIN: auth.admin_payload,
            self.PILOT: auth.pilot_payload
        }

        return methods[self]()
