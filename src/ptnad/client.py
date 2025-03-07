import requests
import warnings
from typing import Literal, Optional, overload
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urljoin
from .exceptions import (
    PTNADAPIError,
)
from .auth import Auth, LocalAuth, SSOAuth
from .api.monitoring import MonitoringAPI
from .api.signatures import SignaturesAPI
from .api.replists import RepListsAPI
from .api.bql import BQLAPI

class PTNADClient:
    def __init__(self, base_url: str, verify_ssl: bool = True):
        self.base_url = base_url.rstrip('/') + '/api/v2/'
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        if not self.verify_ssl:
            warnings.simplefilter('ignore', InsecureRequestWarning)
        self.csrf_token = None
        self.auth = Auth(self)
        self.monitoring = MonitoringAPI(self)
        self.signatures = SignaturesAPI(self)
        self.replists = RepListsAPI(self)
        self.bql = BQLAPI(self)

    @overload
    def set_auth(self, auth_type: Literal['local'], *, username: str, password: str) -> None:
        ...

    @overload
    def set_auth(self, auth_type: Literal['sso'], *,
                sso_url: str, client_id: str, client_secret: str,
                username: str, password: str) -> None:
        ...

    def set_auth(self, auth_type: str = 'local', **kwargs):
        if auth_type == 'local':
            self.auth.set_strategy(LocalAuth(**kwargs))
        elif auth_type == 'sso':
            self.auth.set_strategy(SSOAuth(**kwargs))
        else:
            raise ValueError(f"Unsupported auth type: {auth_type}")

    def login(self):
        self.auth.login()
        self.csrf_token = self.session.cookies.get('csrftoken')

    def logout(self):
        self.auth.logout()
        self.csrf_token = None

    def request(self, method: str, endpoint: str, **kwargs):
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        headers = kwargs.pop('headers', {})
        if self.csrf_token:
            headers['X-CSRFToken'] = self.csrf_token
        headers['Referer'] = self.base_url

        response = None
        try:
            response = self.session.request(method, url, headers=headers, **kwargs)
            if response.status_code >= 400:
                self._handle_http_error(response)
            return response
        except requests.exceptions.RequestException as e:
            self._handle_request_exception(e, response)


    def _handle_request_exception(self, exception, response):
        if isinstance(exception, requests.exceptions.SSLError):
            raise ConnectionError("SSL certificate verification failed")
        elif isinstance(exception, requests.exceptions.Timeout):
            raise TimeoutError("Request timed out")
        elif isinstance(exception, requests.exceptions.ConnectionError):
            raise ConnectionError("Connection error occurred")
        else:
            raise PTNADAPIError(f"Unexpected error: {str(exception)}")

    def _handle_http_error(self, response):
        error_message = f"HTTP error occurred: {response.status_code} {response.reason}. Response content: {response.text}"
        raise PTNADAPIError(error_message, status_code=response.status_code, response=response)

    def get(self, endpoint: str, **kwargs):
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self.request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self.request('PUT', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.request('DELETE', endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        return self.request('PATCH', endpoint, **kwargs)
