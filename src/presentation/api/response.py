from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")


def create_error_response(
    status_code: int, message: str, data: T | None = None
):
    response = UnifiedResponse[T](
        isSuccess=False, statusCode=status_code, message=message, data=data
    )
    return response


def create_success_response(
    status_code: int, message: str = "", data: T | None = None
):
    response = UnifiedResponse[T](
        isSuccess=True, statusCode=status_code, message=message, data=data
    )
    return response


class UnifiedResponse(BaseModel, Generic[T]):
    isSuccess: bool = True
    statusCode: int = 200
    data: T | None = None
    message: str = ""


class BaseResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )
