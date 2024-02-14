#!/usr/bin/env python3
"""basic auth"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


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
