#!/usr/bin/env python3
"""filter datum function"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(
            f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message
        )
    return message
