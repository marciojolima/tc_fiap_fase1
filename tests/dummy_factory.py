import random

import factory
from factory.alchemy import SQLAlchemyModelFactory

from api_books_tc.models import Book, User


class BookFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    price = factory.LazyFunction(lambda: round(random.uniform(1, 100), 2))
    category = factory.Iterator(['Fiction', 'Non-Fiction', 'Mystery', 'Science'])
    rating = factory.LazyAttribute(lambda n: round(random.uniform(1.0, 5.0), 1))
    image_url = factory.Faker('image_url')
    availability = factory.Faker('boolean')


class UserBaseNoModel:
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password', length=16, special_chars=True)
    is_admin = False


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password', length=16, special_chars=True)
    is_admin = False
