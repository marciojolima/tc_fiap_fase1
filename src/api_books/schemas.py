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
    availability: int = Field(..., description='Disponibilidade do livro')
    category: str = Field(..., description='Categoria do livro')
    image_url: Optional[str] = Field(None, description='URL da imagem do livro')
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'title': 'The Great Adventure',
                'price': 29.99,
                'rating': 4.5,
                'availability': 5,
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
                        'availability': 22,
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
    access_token: str = Field(
        ...,
        min_length=1,
        description='Token JWT para autenticação da API',
        examples=[
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEyMyIsImV4cCI6MTY0MDk5NTIwMH0.abc123',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0MDk5NTIwMH0.def456',
        ],
    )
    token_type: str = Field(
        default='Bearer',
        description='Tipo do token de autenticação (sempre Bearer para JWT)',
        examples=['Bearer'],
    )
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'access_token': (
                    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                    'eyJzdWIiOiJ1c2VyXzEyMyIsImV4cCI6MTY0MDk5NTIwMH0.'
                    'signature'
                ),
                'token_type': 'Bearer',
            }
        },
    )


class Login_Token(Token):
    refresh_token: str = Field(
        ...,
        min_length=1,
        description='Token de renovação para obter novos access tokens sem re-login',
        examples=['rt_abc123xyz789refresh_token_example', 'rt_def456uvw012another_refresh_token'],
    )
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'access_token': (
                    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                    'eyJzdWIiOiJ1c2VyXzEyMyIsImV4cCI6MTY0MDk5NTIwMH0.'
                    'signature'
                ),
                'token_type': 'Bearer',
                'refresh_token': 'rt_abc123xyz789refresh_token_example_long_string',
            }
        },
    )


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


class MLFeature(BaseModel):
    x1_availability: int = Field(..., description='entrada: quantidade em estoque')
    x2_rating: float = Field(..., description='entrada: nota média do livro')
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'x1_availability': 22,
                'x2_rating': 5,
            }
        },
    )


class MLTraining_Data(BaseModel):
    x1_availability: int = Field(..., description='entrada: quantidade em estoque')
    x2_rating: float = Field(..., description='entrada: nota média do livro')
    y_label_price: float = Field(..., description='saída: preço')
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {'x1_availability': 4, 'x2_rating': 4, 'y_labels_price': 28.07}
        },
    )


class MLTraining_DataList(BaseModel):
    training: List[MLTraining_Data] = Field(..., description='Dados para treino')
    test: List[MLTraining_Data] = Field(..., description='Dados para test')
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'training': [
                {'x1_availability': 22, 'x2_rating': 3, 'y_label_price': 51.77},
                {'x1_availability': 20, 'x2_rating': 1, 'y_label_price': 50.1},
            ],
            'test': [{'x1_availability': 22, 'x2_rating': 4, 'y_label_price': 33.23}],
        },
    )


class PredictionInput(BaseModel):
    x1_availability: int = Field(
        ...,
        ge=0,
        le=100,
        description='Quantidade disponível em estoque do livro',
        examples=[10, 25, 50],
    )
    x2_rating: float = Field(
        ...,
        ge=1.0,
        le=5.0,
        description='Avaliação média do livro (1.0 a 5.0 estrelas)',
        examples=[3.5, 4.2, 4.8],
    )
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={'example': {'x1_availability': 15, 'x2_rating': 4.3}},
    )


class PredictionOutput(BaseModel):
    predicted_price: float = Field(
        ...,
        ge=0.0,
        description='Preço previsto pelo modelo em reais (R$)',
        examples=[45.50, 78.90, 120.00],
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description='Nível de confiança da predição (0.0 a 1.0)',
        examples=[0.85, 0.92, 0.78],
    )
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={'example': {'predicted_price': 87.50, 'confidence': 0.89}},
    )
