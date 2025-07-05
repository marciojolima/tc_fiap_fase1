from fastapi import Depends
from sqlalchemy.orm import Session

from api_books_tc.database.connection import get_session
from api_books_tc.models import User
from api_books_tc.security import get_hash_from_password


class UserDataBase:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.model = User

    def create_user(self, username: str, password: str, email: str, is_admin: bool) -> User:
        hashed = get_hash_from_password(password)
        new_user = self.model(username=username, password=hashed, email=email, is_admin=is_admin)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
