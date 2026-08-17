import base64
import hashlib
import hmac
import json
from urllib.parse import urlencode

import jwt
import requests

from app.config import Config
from app.repositories.author_repository import AuthorRepository


class LinkedInOAuthService:

    AUTHORIZATION_URL = (
        "https://www.linkedin.com/oauth/v2/authorization"
    )

    TOKEN_URL = (
        "https://www.linkedin.com/oauth/v2/accessToken"
    )

    SCOPE = "openid profile email w_member_social"

    def __init__(self):

        self.author_repository = AuthorRepository()

    def _create_state(self, author_id: str) -> str:

        payload = {
            "author_id": author_id
        }

        payload_json = json.dumps(
            payload,
            separators=(",", ":")
        )

        payload_encoded = base64.urlsafe_b64encode(
            payload_json.encode()
        ).decode().rstrip("=")

        signature = hmac.new(
            Config.LINKEDIN_CLIENT_SECRET.encode(),
            payload_encoded.encode(),
            hashlib.sha256,
        ).hexdigest()

        return f"{payload_encoded}.{signature}"

    def _read_state(self, state: str) -> str:

        try:

            payload_encoded, signature = state.split(".", 1)

            expected_signature = hmac.new(
                Config.LINKEDIN_CLIENT_SECRET.encode(),
                payload_encoded.encode(),
                hashlib.sha256,
            ).hexdigest()

            if not hmac.compare_digest(
                signature,
                expected_signature
            ):
                raise ValueError("Invalid OAuth state.")

            padding = "=" * (
                4 - len(payload_encoded) % 4
            )

            payload_json = base64.urlsafe_b64decode(
                payload_encoded + padding
            ).decode()

            payload = json.loads(payload_json)

            author_id = payload.get("author_id")

            if not author_id:
                raise ValueError(
                    "Missing author ID in OAuth state."
                )

            return author_id

        except Exception as e:

            raise ValueError(
                f"Invalid OAuth state: {e}"
            )

    def get_authorization_url(self, author_id: str) -> str:

        state = self._create_state(author_id)

        params = {
            "response_type": "code",
            "client_id": Config.LINKEDIN_CLIENT_ID,
            "redirect_uri": Config.LINKEDIN_REDIRECT_URI,
            "state": state,
            "scope": self.SCOPE,
        }

        return (
            f"{self.AUTHORIZATION_URL}?"
            f"{urlencode(params)}"
        )

    def handle_callback(self, code: str, state: str):

        author_id = self._read_state(state)

        response = requests.post(
            self.TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": Config.LINKEDIN_REDIRECT_URI,
                "client_id": Config.LINKEDIN_CLIENT_ID,
                "client_secret": Config.LINKEDIN_CLIENT_SECRET,
            },
            timeout=30,
        )

        response.raise_for_status()

        token = response.json()

        access_token = token.get("access_token")

        if not access_token:
            raise Exception(
                "LinkedIn did not return an access token."
            )

        refresh_token = token.get(
            "refresh_token",
            ""
        )

        id_token = token.get("id_token")

        if not id_token:
            raise Exception(
                "LinkedIn did not return an ID token."
            )

        claims = jwt.decode(
            id_token,
            options={
                "verify_signature": False
            },
        )

        person_id = claims.get("sub")

        if not person_id:
            raise Exception(
                "LinkedIn Person ID was not found in ID token."
            )

        self.author_repository.update_linkedin_credentials(
            page_id=author_id,
            access_token=access_token,
            refresh_token=refresh_token,
            person_id=person_id,
        )

        return {
            "author_id": author_id,
            "person_id": person_id,
        }
