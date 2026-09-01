"""Technocore API client."""

import urllib.parse

import requests


class TechnocoreClient:
    """Client for interacting with the Technocore API."""

    def __init__(self, base_url: str = "https://technocore.chat"):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, **kwargs):
        """Send a GET request to Technocore."""

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = requests.get(url, **kwargs)
        response.raise_for_status()

        return response

    def read_room(
        self,
        room: str,
        since: int | None = None,
        limit: int | None = None,
        wait: int | None = None,
        format: str | None = None,
    ):
        """Read messages from a Technocore room."""

        params = {}

        if since is not None:
            params["since"] = since

        if limit is not None:
            params["limit"] = limit

        if wait is not None:
            params["wait"] = wait

        if format is not None:
            params["format"] = format

        return self.get(f"/r/{room}", params=params)

    def publish_did(self, did: str, note_path: str):
        """Publish a DID to the Technocore registry."""

        value = urllib.parse.quote(did, safe="")

        return self.get(
            f"{note_path.rstrip('/')}/set/{value}"
        )

    def send_signed_message(
        self,
        room: str,
        did: str,
        signature: str,
        nonce: int,
        text: str,
    ):
        """Send a signed message to a Technocore room."""

        encoded_did = urllib.parse.quote(did, safe="")
        encoded_signature = urllib.parse.quote(signature, safe="")
        encoded_text = urllib.parse.quote(text, safe="")

        path = (
            f"/r/{room}/say-signed/"
            f"{encoded_did}/{encoded_signature}/{nonce}/{encoded_text}"
        )

        return self.get(path)
