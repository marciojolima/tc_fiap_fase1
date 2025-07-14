from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool
    model_config = ConfigDict(
        from_attributes=True,
        exclude={'id'},
        json_schema_extra={
            'username': 'username',
            'email': 'tcchall@example.com',
            'password': 'secret',
            'is_admin': False,
        },
    )


class UserResponse(UserBase):
    id: int
    password: str = Field(exclude=True)
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    total: int = Field(description='Número total de usuários')
    users: List[UserResponse] = Field(..., description='Lista de usuários')
    model_config = ConfigDict(from_attributes=True)


class UserCreated(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookSchema(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BooksList(BaseModel):
    total: int = Field(description='Número total de livros')
    books: List[BookSchema] = Field(..., description='Lista de livros')
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'total': 2,
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
    total: int = Field(description='Número total de categorias')
    categories: List[str] = Field(description='Lista de categorias')

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'total': 5,
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
    title: str | None = Field(default=None, min_length=0, max_length=30)
    category: str | None = Field(default=None)


class FilterCategory(BaseModel):
    name: str | None = Field(default=None, min_length=0, max_length=20)


class StatusServico(str, Enum):
    UP = 'up'
    DOWN = 'down'


class StatusDependencia(BaseModel):
    status: StatusServico = Field(description="O estado atual da dependência ('up' ou 'down').")
    error: Optional[str] = Field(None, description="Mensagem de erro, caso o status seja 'down'.")
    model_config = ConfigDict(from_attributes=True)


class RespostaHealthCheck(BaseModel):
    api_status: StatusServico = Field(description='O estado geral da API.')
    database: StatusDependencia = Field(description='O estado da conexão com o banco de dados.')
    internet_connectivity: StatusDependencia = Field(
        description='O estado da conectividade com a internet.'
    )
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'api_status': 'up',
            'dependencies': {
                'database': {'status': 'up', 'error': None},
                'internet_connectivity': {'status': 'up', 'error': None},
            },
        },
    )


class Token(BaseModel):
    access_token: str
    token_type: str  # Bearer


class StatsCategories(BaseModel):
    total_categories: int = Field(description='Número total de categorias')
    categories_count_distribution: Dict = Field(
        description='Quantidade de livros em cada categoria'
    )
    categories_avg_price_distribution: Dict = Field(
        description='Preço médio de livros em cada categoria'
    )

    model_config = ConfigDict(from_attributes=True)


class StatsOverview(BaseModel):
    total_books: int = Field(description='Total de livros disponíveis')
    average_price: float = Field(description='Preço médio dos livros')
    count_categories: int = Field(description='Quantidade de livros disponíveis')
    rating_distribuition: Dict = Field(description='Distribuição de livros por avaliação')

    model_config = ConfigDict(from_attributes=True)


class FilterStatPriceRange(BaseModel):
    min_price: float = Field(default=0.0, ge=0, description='Preço mínimo do livro')
    max_price: float | None = Field(default=None, description='Preço máximo do livro')


class StatsPriceRange(BaseModel):
    total: int = Field(description='Número total de livros')
    books: List[BookSchema] = Field(..., description='Lista de livros')
    model_config = ConfigDict(from_attributes=True)
