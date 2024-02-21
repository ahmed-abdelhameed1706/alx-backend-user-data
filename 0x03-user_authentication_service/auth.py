#!/usr/bin/env python3
"""Auth module
"""
from db import DB
from bcrypt import hashpw, gensalt, checkpw
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """Generate a uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """takes email and password and registers a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if a user is valid"""
        try:
            user = self._db.find_user_by(email=email)
            if user and checkpw(
                password.encode("utf-8"), user.hashed_password
            ):  # no pep8
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """create session id for users"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """get user from session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None
