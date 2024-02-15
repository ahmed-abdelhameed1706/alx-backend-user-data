#!/usr/bin/env python3
"""auth class"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """reqire auth method"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        for excluded in excluded_paths:
            if excluded.endswith("*"):
                if path.startswith(excluded[:-1]):
                    return False
            else:
                if not path.endswith("/"):
                    path += "/"
                if path == excluded:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header method"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):  # type: ignore
        """current user method"""
        return None

    def session_cookie(self, request=None):
        """return cookie from a request"""
        if request is None:
            return None
        if getenv("SESSION_NAME") in request.cookies:
            return request.cookies.get(getenv("SESSION_NAME"))
        return None
