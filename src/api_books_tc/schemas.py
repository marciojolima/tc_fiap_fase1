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
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'title': 'The Great Adventure',
                'price': 29.99,
                'rating': 4.5,
                'availability': True,
                'category': 'Fiction',
                'image_url': 'https://example.com/book.jpg',
            }
        },
    )


class BookSchema(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BooksList(BaseModel):
    count_books: int = Field(description='Número total de livros')
    books: List[BookSchema] = Field(..., description='Lista de livros')
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'count_books': 2,
                'books': [
                    {
                        'id': 1,
                        'title': 'The Great Adventure',
                        'price': 29.99,
                        'rating': 4.5,
                        'availability': True,
                        'category': 'Fiction',
                        'image_url': 'https://example.com/book1.jpg',
                    },
                    {
                        'id': 2,
                        'title': 'History Unveiled',
                        'price': 39.99,
                        'rating': 4.0,
                        'availability': False,
                        'category': 'History',
                        'image_url': 'https://example.com/book2.jpg',
                    },
                ],
            }
        },
    )


class CategoriesList(BaseModel):
    count_categories: int = Field(description='Número total de categorias')
    categories: List[str] = Field(description='Lista de categorias')

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'count_categories': 5,
                'categories': ['Biography', 'Fantasy', 'Fiction', 'History', 'Science'],
            }
        },
    )


class FilterPage(BaseModel):
    offset: int = Field(default=None, ge=0, description='Número de registros a pular (offset)')
    limit: int = Field(
        default=None, ge=0, description='Número máximo de registros a retornar (limit)'
    )


class FilterBook(FilterPage):
    title: str | None = Field(default=None, min_length=5, max_length=30)
    category: str | None = Field(default=None)


class FilterCategory(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=20)
