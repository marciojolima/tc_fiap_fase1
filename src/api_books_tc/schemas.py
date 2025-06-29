from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


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
    availability: bool = Field(..., description='Disponibilidade do livro')
    category: str = Field(..., description='Categoria do livro')
    image_url: Optional[str] = Field(None, description='URL da imagem do livro')
    model_config = ConfigDict(from_attributes=True)


class BookSchema(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BooksList(BaseModel):
    count_books: int
    books: List[BookSchema]
    model_config = ConfigDict(from_attributes=True)


class FilterPage(BaseModel):
    offset: int = Field(default=None, ge=0, description='Número de registros a pular (offset)')
    limit: int = Field(
        default=None, ge=0, description='Número máximo de registros a retornar (limit)'
    )


class FilterBook(FilterPage):
    title: str | None = Field(default=None, min_length=5, max_length=20)
    category: str | None = Field(default=None)
