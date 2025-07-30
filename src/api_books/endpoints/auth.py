from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api_books.database.users import UserDataBase
from api_books.schemas import Login_Token, Token
from api_books.security.auth import (
    create_access_token,
    create_refresh_token,
    get_user_refreshed_tokenizer,
)
from api_books.security.crypt import is_valid_password

router = APIRouter(prefix='/api/v1/auth', tags=['Auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
DBService = Annotated[UserDataBase, Depends()]


@router.post(
    '/login',
    status_code=HTTPStatus.OK,
    response_model=Login_Token,
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

    access_token = create_access_token(claims={'sub': user.username})
    refresh_token = create_refresh_token(claims={'sub': user.username})

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@router.post(
    '/refresh',
    status_code=HTTPStatus.OK,
    response_model=Token,
    summary='Gera um novo access_token usando refresh_token.',
)
def refresh_access_token(current_user=Depends(get_user_refreshed_tokenizer)):
    """
    Recebe um refresh token no header de autorização (Bearer) e retorna
    um novo access token.
    """

    new_access_token = create_access_token(claims={'sub': current_user.username})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
