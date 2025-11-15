from fastapi import APIRouter, Depends
from starlette import status

from src.application.usecases.orders.dto import OrderDTO
from src.application.usecases.orders.usecases import OrderInteractor
from src.presentation.api.orders.schema import CreateOrder
from src.presentation.api.response import (
    UnifiedResponse,
    create_success_response,
)
from src.presentation.services import get_order_interactor

router = APIRouter()


@router.post("")
async def create_order(
    schema: CreateOrder,
    interactor: OrderInteractor = Depends(get_order_interactor),
) -> UnifiedResponse[OrderDTO]:
    order = await interactor.create_order(dto=schema)
    return create_success_response(data=order, status_code=status.HTTP_200_OK)
