from typing import List, Tuple

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session, defer

from api_books_tc.database.connection import get_session
from api_books_tc.models import User
from api_books_tc.security.crypt import get_hash_from_password


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

    def find_user_by_username_or_email(self, username: str = None, email: str = None) -> User:
        query = select(self.model)
        query = query.where((self.model.username == username) | (self.model.email == email))
        user = self.session.scalar(query)
        return user

    def get_all_users(self) -> Tuple[int, List[User]]:
        query = select(self.model).options(defer(self.model.password))  # exceto password
        users = self.session.scalars(query).all()
        count_users = self.session.scalar(select(func.count()).select_from(query.subquery()))
        return count_users, users
