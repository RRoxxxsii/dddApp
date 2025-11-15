from fastapi import APIRouter, Depends
from starlette import status

from src.application.usecases.users.dto import UserDTO
from src.application.usecases.users.usecases import UserInteractor
from src.presentation.api.response import (
    UnifiedResponse,
    create_success_response,
)
from src.presentation.api.users.schema import CreateUser
from src.presentation.services import get_user_interactor

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    schema: CreateUser,
    interactor: UserInteractor = Depends(get_user_interactor),
) -> UnifiedResponse[UserDTO]:
    user = await interactor.create_user(schema)
    return create_success_response(
        data=user,
        status_code=status.HTTP_201_CREATED,
    )
