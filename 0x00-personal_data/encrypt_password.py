#!/usr/bin/env python3
"""encrypt password function"""
import bcrypt


def hash_password(password: str) -> str:
    """returns a hashed password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
