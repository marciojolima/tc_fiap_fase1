from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api_books_tc.database.users import UserDataBase
from api_books_tc.schemas import Token
from api_books_tc.security.auth import create_jwt
from api_books_tc.security.crypt import is_valid_password

router = APIRouter(prefix='/api/v1/auth', tags=['Auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
DBService = Annotated[UserDataBase, Depends()]


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
def login_for_access_token(db: DBService, form_data: OAuth2Form):
    user = db.find_user_by_username_or_email(username=form_data.username)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='username not found')

    if not is_valid_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Incorrect password')

    token = create_jwt(claims={'sub': user.username})

    return {'access_token': token, 'token_type': 'bearer'}
