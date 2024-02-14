#!/usr/bin/env python3
"""auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """reqire auth method"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith("/"):
            path = path + "/"

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """authorization header method"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None

        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar("User"):  # type: ignore
        """current user method"""
        return None
