from fastapi import APIRouter, Depends
from starlette import status

from src.application.analytics.usecases import UserActionAnalyticInteractor
from src.application.users.dto import UserDTO
from src.presentation.api.response import create_success_response, UnifiedResponse
from src.presentation.services import get_user_action_interactor

router = APIRouter()


@router.get("/users")
async def get_user_count(
        interactor: UserActionAnalyticInteractor = Depends(get_user_action_interactor),
) -> UnifiedResponse[int]:
    count = await interactor.get_user_action_count()
    return create_success_response(
        data=count,
        status_code=status.HTTP_200_OK
    )
