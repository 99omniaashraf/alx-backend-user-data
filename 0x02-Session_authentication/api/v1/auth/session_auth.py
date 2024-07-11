#!/usr/bin/env python3
"""Session Class"""
from api.v1.auth.auth import Auth
from api.v1.views.users import User
import uuid


class SessionAuth(Auth):
    """Define SessionAuth class"""
    user_id_by_session_id = {}

    def __init__(self):
        """Initialize SessionAuth class"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
            returns a User instance based on a cookie value
        """
        if not request:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
            deletes the user session / logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user = self.user_id_for_session_id(session_id)
        if not user:
            return False
        del self.user_id_by_session_id[session_id]
        return True
