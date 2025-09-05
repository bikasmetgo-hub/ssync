from abc import ABC, abstractmethod
from typing import Dict

class BaseIntegration(ABC):
    @abstractmethod
    def get_authorization_url(self, state: str) -> str:
        """Return the URL to redirect user for OAuth login."""

    @abstractmethod
    def exchange_code_for_token(self, code: str) -> Dict:
        """Exchange the OAuth code for access and refresh tokens."""

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> Dict:
        """Refresh expired access token."""

    @abstractmethod
    def get_user_profile(self, access_token: str) -> Dict:
        """Get the connected account's profile info."""
