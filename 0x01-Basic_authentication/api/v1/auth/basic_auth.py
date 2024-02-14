#!/usr/bin/env python3
"""basic auth"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """basic auth class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extracting method for base64"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """decoding method for base64"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)

        except Exception:
            return None

        return decoded.decode("utf-8")

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):  # type: ignore
        """extract user creds"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        return (
            decoded_base64_authorization_header.split(":")[0],
            decoded_base64_authorization_header.split(":")[1],
        )

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar("User"):  # type: ignore
        """get user from credentials"""
        if user_email is None or not isinstance(user_email, str):
            return
        if user_pwd is None or not isinstance(user_email, str):
            return None
        users = User.search({"email": user_email})
        user = None
        if len(users) > 0:
            user = users[0]
            if not user.is_valid_password(user_pwd):
                return None
        return user
