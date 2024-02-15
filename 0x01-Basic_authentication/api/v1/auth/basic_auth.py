#!/usr/bin/env python3
"""basic auth"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """basic auth class"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:  # no pep8
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

        splitted_header = decoded_base64_authorization_header.split(":")
        username = splitted_header[0]
        password = " ".join(splitted_header[1:])

        return (username, password)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):  # no pep 8 # type: ignore
        """get user from credentials"""
        if user_email is None or not isinstance(user_email, str):
            return
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        user = None
        if len(users) > 0:
            user = users[0]
            if not user.is_valid_password(user_pwd):
                return None
        return

    def current_user(self, request=None) -> TypeVar("User"):  # type: ignore
        """get current user"""
        header = self.authorization_header(request)
        if not header:
            return None

        base64_header = self.extract_base64_authorization_header(header)
        if not base64_header:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if not decoded_header:
            return None

        user_creds = self.extract_user_credentials(decoded_header)
        if user_creds[0] is None or user_creds[1] is None:
            return None

        return self.user_object_from_credentials(user_creds[0], user_creds[1])
