from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter(prefix='/api/v1/users', tags=['Users'])


@router.get('/', status_code=HTTPStatus.OK)
async def get_user_test():
    return {'teste': 'teste'}
