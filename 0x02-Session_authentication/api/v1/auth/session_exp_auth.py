#!/usr/bin/env python3
"""
Expiration
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Define Expiration Class"""
    def __init__(self):
        """Init Method"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create Session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for Session ID"""
        if not session_id:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return None
        if self.session_duration <= 0:
            return session.get('user_id')
        created_at = session.get('created_at')
        if not created_at:
            return None
        expire = created_at + timedelta(seconds=self.session_duration)
        if expire < datetime.now():
            return None
        return session.get('user_id')
