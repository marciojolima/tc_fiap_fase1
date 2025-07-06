from typing import List, Tuple

from fastapi import Depends
from sqlalchemy import desc, distinct, func, select
from sqlalchemy.orm import Session

from api_books_tc.database.connection import get_session
from api_books_tc.models import Book


class BookDataBase:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.model = Book

    def get_books(
        self, offset: int, limit: int, title: str, category: str
    ) -> Tuple[int, List[Book]]:
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

    def get_books_top_rated(self, offset: int, limit: int) -> Tuple[int, List[Book]]:
        query = select(self.model).distinct().order_by(desc(self.model.rating))

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        books = self.session.scalars(query).all()
        count_books = self.session.scalar(select(func.count()).select_from(query.subquery()))

        return count_books, books

    def get_categories(self, name: str) -> Tuple[int, str]:
        query = select(self.model.category).distinct().order_by(self.model.category)

        if name:
            query = query.filter(self.model.category.contains(name))

        categories = self.session.scalars(query).all()
        count_categories = len(categories)

        return count_categories, categories

    def get_stats_overview(self) -> Tuple[int, float, List[Tuple]]:
        # total livros
        count_query = select(func.count(self.model.id))
        total_books = self.session.scalar(count_query)

        # preço medio
        avg_price_query = select(func.round(func.avg(self.model.price), 2))
        average_price = self.session.scalar(avg_price_query)

        # distribuição de rates
        rating_dist_query = (
            select(self.model.rating, func.count(self.model.id))
            .group_by(self.model.rating)
            .order_by(self.model.rating)
        )
        rating_dist = self.session.execute(rating_dist_query).all()

        return total_books, average_price, rating_dist

    def get_stats_categories(self) -> Tuple[int, List[Tuple], List[Tuple]]:
        # total de categorias
        query_count_categories = select(func.count(distinct(self.model.category)))
        total_categories = self.session.scalar(query_count_categories)

        # distribuição de livros por categoria
        categories_dist_query = (
            select(self.model.category, func.count(self.model.id))
            .group_by(self.model.category)
            .order_by(self.model.category)
        )
        categories_count_dist = self.session.execute(categories_dist_query).all()

        # distribuição do preço médio dentro da cada categoria
        avg_price_query = (
            select(
                self.model.category,
                func.round(func.avg(self.model.price), 2).label('average_price'),
            )
            .group_by(self.model.category)
            .order_by(self.model.category)
        )
        categories_avg_price_dist = self.session.execute(avg_price_query).all()

        return total_categories, categories_count_dist, categories_avg_price_dist

    def get_stats_by_price_range(self, min_price: float = 0.0, max_price: float | None = None):
        if min_price < 0:
            raise ValueError("'min_price' cannot be negative")
        if max_price is not None and max_price < 0:
            raise ValueError("If provided, 'max_price' cannot be negative")

        final_max_price = max_price
        if final_max_price is None:
            print("INFO: 'max_price' não fornecido. Buscando o maior preço no banco...")
            max_db_price_query = select(func.max(self.model.price))
            final_max_price = self.session.scalar(max_db_price_query)
            print(f'INFO: Preço máximo encontrado no banco: R$ {final_max_price:.2f}')

        if min_price >= final_max_price:
            raise ValueError(
                f"'min_price' (R$ {min_price:.2f}) must be less than "
                f"'max_price' (R$ {final_max_price:.2f})."
            )

        query = (
            select(self.model)
            .where(self.model.price.between(min_price, final_max_price))
            .order_by(self.model.price)
        )

        books = self.session.scalars(query).all()
        total_books = len(books)

        return total_books, books
