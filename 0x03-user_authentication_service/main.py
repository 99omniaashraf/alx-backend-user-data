#!/usr/bin/env python3
"""End-to-end integration test of auth service"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://0.0.0.0:5000/"


def register_user(email: str, password: str) -> None:
    """Register a new user"""
    request_body = {"email": email, "password": password}
    url = f"{URL}/users"

    response = requests.post(url, data=request_body)
    if response.status_code == 200:
        assert response.json() == {"email": email, "message": "user created"}
    else:
        assert response.status_code == 400
        assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Login with the wrong password"""
    request_body = {"email": email, "password": password}
    url = f"{URL}/sessions"

    response = requests.post(url, data=request_body)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Login"""
    request_body = {"email": email, "password": password}
    url = f"{URL}/sessions"

    response = requests.post(url, data=request_body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Unable to access profile"""
    url = f"{URL}/profile"

    response = requests.get(url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Have auth to access profile"""
    url = f"{URL}/profile"
    request_body = {"session_id": session_id}

    response = requests.get(url, cookies=request_body)

    assert response.status_code == 200
    assert response.json().get("email")


def log_out(session_id: str) -> None:
    """Logout"""
    url = f"{URL}/sessions"
    request_body = {"session_id": session_id}

    response = requests.delete(url, cookies=request_body)

    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Reset password token"""
    url = f"{URL}/reset_password"
    request_body = {"email": email}

    response = requests.post(url, data=request_body)
    assert response.status_code == 200
    assert response.json().get("email") == email

    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    url = f"{URL}/reset_password"
    request_body = {"email": email, "reset_token": reset_token,
                    "new_password": new_password}

    response = requests.put(url, data=request_body)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
