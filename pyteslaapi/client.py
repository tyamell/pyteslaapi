from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from pyteslaapi.vehicle import Vehicle
from pyteslaapi.exceptions import TeslaException

import logging

_LOGGER = logging.getLogger(__name__)

TESLA_API_BASE_URL = 'https://owner-api.teslamotors.com/'
TOKEN_URL = TESLA_API_BASE_URL + 'oauth/token'
API_URL = TESLA_API_BASE_URL + 'api/1'

OAUTH_CLIENT_ID = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
OAUTH_CLIENT_SECRET = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'

class TeslaApiClient:
    def __init__(self, email, password, wake=False,
                 update_interval=900,
                 drive_interval=45,
                 wake_interval=21800):
        self._email = email
        self._password = password
        self._token = None
        self._vehicles = [Vehicle(self, vehicle, wake,
                                  update_interval,
                                  drive_interval,
                                  wake_interval) for vehicle in self.get('vehicles')]

    def _get_new_token(self):
        request_data = {
            'grant_type': 'password',
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
            'email': self._email,
            'password': self._password
        }

        response = requests.post(TOKEN_URL, data=request_data)
        response_json = response.json()

        if 'response' in response_json:
            raise TeslaException(response.status_code, response_json['response'])

        return response_json

    def _refresh_token(self, refresh_token):
        request_data = {
            'grant_type': 'refresh_token',
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
            'refresh_token': refresh_token,
        }

        response = requests.post(TOKEN_URL, data=request_data)
        response_json = response.json()

        if 'response' in response_json:
            raise TeslaException(response.status_code, response_json['response'])

        return response_json

    def authenticate(self):
        if not self._token:
            self._token = self._get_new_token()

        expiry_time = timedelta(seconds=self._token['expires_in'])
        expiration_date = datetime.fromtimestamp(self._token['created_at']) + expiry_time

        if datetime.utcnow() >= expiration_date:
            self._token = self._refresh_token(self._token['refresh_token'])

    def _get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self._token["access_token"])
        }

    def command(self, vehicle_id, command_name, data={}):
        self.post('vehicles/{}/command/{}'.format(vehicle_id, command_name), data)


    def get(self, endpoint):
        try:
            self.authenticate()

            response = self.__requests_retry_session().get(
                '{}/{}'.format(API_URL, endpoint), headers=self._get_headers()
            )
            response_json = response.json()

            if 'error' in response_json:
                raise TeslaException(response.status_code, response_json['error'])

            return response_json['response']
        except requests.exceptions.RetryError as e:
            _LOGGER.debug(str(e))
            return False


    def post(self, endpoint, data = {}):
        try:
            self.authenticate()

            response = self.__requests_retry_session().post(
                '{}/{}'.format(API_URL, endpoint), headers=self._get_headers(),
                data=data
            )
            response_json = response.json()

            if 'error' in response_json:
                raise TeslaException(response.status_code, response_json['error'])

            return response_json['response']
        except requests.exceptions.RetryError as e:
            _LOGGER.debug(str(e))
            return False

    def __requests_retry_session(self,
        retries=5,
        backoff_factor=1.5,
        status_forcelist=(500, 502, 504, 408),
        session=None,
    ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    @property
    def vehicles(self):
        return self._vehicles


