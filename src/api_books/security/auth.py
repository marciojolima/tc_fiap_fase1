from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash

from api_books.database.users import UserDataBase
from api_books.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()
DBService = Annotated[UserDataBase, Depends()]
# checa se há token no header da requsição
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/token')


def create_jwt(claims: dict) -> str:
    payload = claims.copy()

    now = datetime.now(tz=ZoneInfo('UTC'))
    time_plus = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = now + time_plus

    payload.update({'exp': expire})

    # encode(payload, key, algorithm)
    token = encode(payload=payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token


def get_user_tokenizer(db: DBService, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub_username = payload.get('sub')
        if not sub_username:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        credentials_exception.detail = 'Expired token'
        raise credentials_exception

    user = db.find_user_by_username_or_email(username=sub_username)

    if not user:
        raise credentials_exception

    return user
