#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new user"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Get user filtered by input args"""
        filtered_user = self._session.query(User).filter_by(**kwargs).first()
        if not filtered_user:
            raise NoResultFound

        return filtered_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user by id with input args"""
        try:
            user_by_id = self.find_user_by(id=user_id)
        except NoResultFound:
            return None

        for key, value in kwargs.items():
            if hasattr(user_by_id, key):
                setattr(user_by_id, key, value)
            else:
                raise ValueError

        self._session.commit()
