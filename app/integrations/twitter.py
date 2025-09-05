import os
import requests
from app.integrations.base import BaseIntegration

class TwitterIntegration(BaseIntegration):
    def __init__(self):
        self.client_id = os.getenv("TWITTER_CLIENT_ID")
        self.client_secret = os.getenv("TWITTER_CLIENT_SECRET")
        self.redirect_uri = os.getenv("TWITTER_REDIRECT_URI")
        self.auth_base = "https://twitter.com/i/oauth2/authorize"
        self.token_url = "https://api.twitter.com/2/oauth2/token"

    def get_authorization_url(self, state: str) -> str:
        scopes = "tweet.read tweet.write users.read offline.access"
        return (
            f"{self.auth_base}?response_type=code&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}&scope={scopes}&state={state}"
        )

    def exchange_code_for_token(self, code: str):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        response = requests.post(self.token_url, data=payload)
        response.raise_for_status()
        return response.json()

    def refresh_token(self, refresh_token: str):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response = requests.post(self.token_url, data=payload)
        response.raise_for_status()
        return response.json()

    def get_user_profile(self, access_token: str):
        headers = {"Authorization": f"Bearer {access_token}"}
        resp = requests.get("https://api.twitter.com/2/users/me", headers=headers)
        resp.raise_for_status()
        return resp.json()
