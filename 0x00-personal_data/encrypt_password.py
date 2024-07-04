#!/usr/bin/env python3
""" doc doc doc """
import bcrypt


def hash_password(password: str) -> bytes:
    """doc doc doc"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """doc doc doc"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
