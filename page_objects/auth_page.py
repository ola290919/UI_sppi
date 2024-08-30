import os
import time
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
    _url: str
    _query: dict
    _instance = None
    _lock = Lock()
    _secret_key: str
    tokens: {AuthToken}

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AuthPage, cls).__new__(cls)
                cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self.session = requests.Session()
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._base_url = os.getenv('DEV_API_BASE_URL')
            self.secret_key = os.getenv('DEV_API_SECRET_KEY')
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
                    'expiry_time': time.time() + float(os.getenv('DEV_REFRESH_TOKEN_EXPIRE_MINUTES')) * 60
                }

                return self.tokens[login]['access_token']

        # Create new token
        response = self._make_tokens_request(login, password)

        self.tokens[login] = {
            'access_token': response.access_token,
            'refresh_token': response.refresh_token,
            'expiry_time': time.time() + float(os.getenv('DEV_REFRESH_TOKEN_EXPIRE_MINUTES')) * 60
        }

        return (self.tokens[login]['access_token'], self.tokens[login]['refresh_token'])

    def as_admin(self):

        return self.get_access_refresh_token(os.getenv('DEV_ADMIN_USER'), os.getenv('DEV_ADMIN_PASSWORD'))

    def as_pilot(self):
        return self.get_access_refresh_token(os.getenv('DEV_PILOT_USER'), os.getenv('DEV_PILOT_PASSWORD'))

# auth = AuthPage()
#
# class Auth(Enum):
#     ADMIN = 1
#
#     def go(self):
#         methods = {
#             self.ADMIN: auth.as_admin
#         }
