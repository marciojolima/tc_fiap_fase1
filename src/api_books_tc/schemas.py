from typing import List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str


class MessageStatus(Message):
    api: str
    version: str
    status: str
    description: str


class BookBase(BaseModel):
    title: str = Field(..., description='Título do livro')
    price: float = Field(..., ge=0, description='Preço do livro')
    rating: float = Field(..., ge=0, le=5, description='Avaliação do livro (0-5)')
    availability: str = Field(..., description='Disponibilidade do livro')
    category: str = Field(..., description='Categoria do livro')
    image_url: Optional[str] = Field(None, description='URL da imagem do livro')


class Book(BookBase):
    id: int


class BooksList(BaseModel):
    count_books: int
    books: List[Book]


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class FilterBook(FilterPage):
    title: str | None = Field(default=None, min_length=5, max_length=20)
    category: str | None = Field(default=None)
