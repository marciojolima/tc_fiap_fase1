from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api_books_tc.database.users import UserDataBase
from api_books_tc.schemas import UserBase, UserList, UserResponse

router = APIRouter(prefix='/api/v1/users', tags=['Users'])

DBService = Annotated[UserDataBase, Depends()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def create_user(userschema: UserBase, db: DBService):
    queried_user = db.find_user_by_username_or_email(
        username=userschema.username, email=userschema.email
    )

    if queried_user:
        if queried_user.username == userschema.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Username already exists')
        if queried_user.email == userschema.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email already exists')

    new_user = db.create_user(
        username=userschema.username,
        password=userschema.password,
        email=userschema.email,
        is_admin=userschema.is_admin,
    )
    return new_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users(db: DBService):
    total, users = db.get_all_users()

    return {'users': users, 'total': total}
