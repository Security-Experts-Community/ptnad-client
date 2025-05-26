from abc import ABC, abstractmethod
from typing import Any

from ptnad.exceptions import AuthenticationError


class AuthStrategy(ABC):
    @abstractmethod
    def authenticate(self, client: Any) -> None:
        pass

    @abstractmethod
    def deauthenticate(self, client: Any) -> None:
        pass


class LocalAuth(AuthStrategy):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def authenticate(self, client: Any) -> None:
        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self._perform_login(client, data)
        self._validate_response(response)

        # Verify authentication by checking status
        client.get("monitoring/status")

    def _perform_login(self, client: Any, data: dict) -> Any:
        try:
            response = client.post("/auth/login", json=data)
            return response
        except Exception as e:
            raise AuthenticationError(f"Local Authentication failed: {str(e)}")

    def _validate_response(self, response: Any) -> None:
        if response.status_code != 200:
            raise AuthenticationError(
                f"Authentication failed with status code: {response.status_code}"
            )

    def deauthenticate(self, client: Any) -> None:
        try:
            client.post("/auth/logout")
        except Exception as e:
            raise AuthenticationError(f"Local Logout failed: {str(e)}")


class SSOAuth(AuthStrategy):
    def __init__(
        self,
        sso_url: str,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        sso_type: str | None = None
    ) -> None:
        self.sso_url = sso_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.sso_type = sso_type

    def authenticate(self, client: Any) -> None:
        auth_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password",
            "response_type": "code id_token",
            "scope": (
                f"openid profile offline_access authorization {self.client_id}.api"
            ),
            "username": self.username,
            "password": self.password,
        }

        # Add amr parameter if sso_type is ldap
        if self.sso_type == "ldap":
            auth_data["amr"] = "ldap"

        response = client.session.post(
            f"{self.sso_url}/connect/token",
            data=auth_data,
            verify=False
        )
        if response.status_code >= 400:
            raise AuthenticationError(f"SSO Authentication failed: {str(response.text)}")

        client.session.headers.update(
            {"Authorization": f"Bearer {response.json()['access_token']}"}
        )

        try:
            # Verify authentication by checking status
            client.get("monitoring/status")
        except Exception as e:
            raise AuthenticationError(f"Failed to authenticate with SSO Token in PT NAD: {str(e)}")

    def deauthenticate(self, client: Any) -> None:
        try:
            client.session.headers.pop("Authorization", None)
            client.session.cookies.clear()
        except Exception as e:
            raise AuthenticationError(f"SSO Logout failed: {str(e)}")


class ApiKeyAuth(AuthStrategy):
    def __init__(
        self,
        apikey: str
    ) -> None:
        self.api_key = apikey

    def authenticate(self, client: Any) -> None:
        client.session.headers.update(
            {"Authorization": f"Bearer {self.api_key}"}
        )

        try:
            # Verify authentication by checking status
            client.get("monitoring/status")
        except Exception as e:
            raise AuthenticationError(f"Failed to authenticate with API Key: {str(e)}")

    def deauthenticate(self, client: Any) -> None:
        try:
            client.session.headers.pop("Authorization", None)
            client.session.cookies.clear()
        except Exception as e:
            raise AuthenticationError(f"Logout failed: {str(e)}")


class Auth:
    def __init__(self, client: Any) -> None:
        self.client = client
        self.strategy: AuthStrategy | None = None

    def set_strategy(self, strategy: AuthStrategy) -> None:
        self.strategy = strategy

    def login(self) -> None:
        if self.strategy is None:
            raise AuthenticationError(
                "Authentication type not set. Use set_auth() first."
            )
        self.strategy.authenticate(self.client)

    def logout(self) -> None:
        if self.strategy is None:
            raise AuthenticationError(
                "Authentication type not set. Use set_auth() first."
            )
        self.strategy.deauthenticate(self.client)
