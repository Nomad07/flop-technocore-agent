"""Technocore API client."""

import requests


class TechnocoreClient:
    """Client for interacting with the Technocore API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, **kwargs):
        """Send a GET request to Technocore."""

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = requests.get(url, **kwargs)
        response.raise_for_status()

        return response
