from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from api_books_tc.database.users import UserDataBase
from api_books_tc.schemas import UserBase, UserResponse

router = APIRouter(prefix='/api/v1/users', tags=['Users'])

DBService = Annotated[UserDataBase, Depends()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def create_user(userSchema: UserBase, db: DBService):
    new_user = db.create_user(
        username=userSchema.username,
        password=userSchema.password,
        email=userSchema.email,
        is_admin=userSchema.is_admin,
    )
    return new_user
