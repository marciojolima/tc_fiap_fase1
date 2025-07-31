import random
from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query

from api_books.database.books import BookDataBase
from api_books.ml_model import fake_model
from api_books.schemas import (
    FilterBook,
    MLFeature,
    MLTraining_DataList,
    PredictionInput,
    PredictionOutput,
)

router = APIRouter(prefix='/api/v1/ml', tags=['ML Ready'])

FilterQueryBooks = Annotated[FilterBook, Query()]
DBService = Annotated[BookDataBase, Depends()]


@router.get(
    '/features/',
    status_code=HTTPStatus.OK,
    response_model=List[MLFeature],
    summary='Extrai features prontas para modelos de Machine Learning.',
)
def get_features(db: DBService, param_request: FilterQueryBooks):
    """
     Retorna um conjunto de dados simplificado contendo apenas as features
    `availability` e `rating`, que podem ser usadas para treinar um modelo de ML.
    """
    _, books = db.get_books(
        title=param_request.title,
        category=param_request.category,
        offset=param_request.offset,
        limit=param_request.limit,
    )

    features = []
    for book in books:
        feature = {'x1_availability': book.availability, 'x2_rating': book.rating}
        features.append(feature)
    return features


@router.get(
    '/training-data/',
    status_code=HTTPStatus.OK,
    response_model=MLTraining_DataList,
    summary='Fornece um conjunto de dados de treinamento (features + label).',
)
def get_training_data(db: DBService):
    """
    Retorna uma amostra de 80% dos dados, contendo as features (`availability`, `rating`)
    e o label (`price`), pronto para ser usado no treinamento de um modelo
    de regressão para prever o preço.
    """
    _, books = db.get_books()

    # Listas para armazenar os dados de treinamento (80%) e os dados restantes (20%)
    training_features = []
    test_features = []
    training_probability = 0.8

    # Iterar sobre o ScalarResult uma única vez
    for book in books:
        feature = {
            'x1_availability': book.availability,
            'x2_rating': book.rating,
            'y_label_price': book.price,
        }
        # Decidir aleatoriamente se o item vai para treinamento (80%) ou restante (20%)
        if random.random() < training_probability:
            training_features.append(feature)
        else:
            test_features.append(feature)

    # Verificar se há dados suficientes
    if not training_features and not test_features:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum livro encontrado',
        )

    return {'training': training_features, 'test': test_features}


@router.post(
    '/predictions/',
    status_code=HTTPStatus.OK,
    response_model=PredictionOutput,
    summary='Prevê o preço de um livro com base em suas features.',
)
async def get_predictions(input: PredictionInput):
    """
    Recebe a disponibilidade (`availability`) e a avaliação (`rating`) de um livro
    e utiliza um modelo de Machine Learning (simulado) para prever seu preço.
    """
    try:
        return fake_model(input)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Features inválidas ou erro na predição'
        )
