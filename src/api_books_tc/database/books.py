from fastapi import Depends
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from api_books_tc.database.connection import get_session
from api_books_tc.models import Book


class BookDataBase:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.model = Book

    def get_books(self, offset: int, limit: int, title: str, category: str):
        query = select(self.model)

        if title:
            query = query.filter(self.model.title.contains(title))

        if category:
            query = query.filter(self.model.category.contains(category))

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        books = self.session.scalars(query).all()
        count_books = self.session.scalar(select(func.count()).select_from(query.subquery()))

        return count_books, books

    def get_book_by_id(self, book_id: int):
        if book_id is None:
            raise ValueError('ID cannot be null.')
        if not isinstance(book_id, int) or book_id <= 0:
            raise ValueError('ID must be positive')

        query = select(self.model).where(self.model.id == book_id)
        book = self.session.scalar(query)

        if book is None:
            raise ValueError(f'Book id: {book_id} not found.')

        return book

    def get_books_top_rated(self):
        query = select(self.model).distinct().order_by(desc(self.model.rating))

        books = self.session.scalars(query).all()
        count_books = self.session.scalar(select(func.count()).select_from(query.subquery()))

        return count_books, books

    def get_categories(self, name: str):
        query = select(self.model.category).distinct().order_by(self.model.category)

        if name:
            query = query.filter(self.model.category.contains(name))

        categories = self.session.scalars(query).all()
        count_categories = len(categories)

        return count_categories, categories
