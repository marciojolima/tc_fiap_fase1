from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api_books.database.users import UserDataBase
from api_books.schemas import Token
from api_books.security.auth import create_jwt
from api_books.security.crypt import is_valid_password

router = APIRouter(prefix='/api/v1/auth', tags=['Auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
DBService = Annotated[UserDataBase, Depends()]


@router.post(
    '/token',
    status_code=HTTPStatus.OK,
    response_model=Token,
    summary='Autentica um usuário e retorna um token JWT.',
)
def login_for_access_token(db: DBService, form_data: OAuth2Form):
    """
    Recebe credenciais de usuário (username e password) via formulário OAuth2.
    """
    user = db.find_user_by_username_or_email(username=form_data.username)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='username not found')

    if not is_valid_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Incorrect password')

    token = create_jwt(claims={'sub': user.username})

    return {'access_token': token, 'token_type': 'bearer'}
