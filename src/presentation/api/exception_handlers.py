from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.domain.exceptions import (
    AlreadyExistsException,
    DomainException,
    InvalidOperationException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from src.presentation.api.response import create_error_response


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(ValidationException)
    async def validation_handler(request: Request, exc: ValidationException):
        return JSONResponse(
            content=(
                create_error_response(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    exc.message,
                ).model_dump()
            ),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            content=(
                create_error_response(
                    status.HTTP_404_NOT_FOUND,
                    exc.message,
                ).model_dump()
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    @app.exception_handler(AlreadyExistsException)
    async def already_exists_handler(
        request: Request, exc: AlreadyExistsException
    ):
        return JSONResponse(
            content=(
                create_error_response(
                    status.HTTP_409_CONFLICT,
                    exc.message,
                ).model_dump()
            ),
            status_code=status.HTTP_409_CONFLICT,
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(
        request: Request, exc: UnauthorizedException
    ):
        return JSONResponse(
            content=(
                create_error_response(
                    status.HTTP_401_UNAUTHORIZED,
                    exc.message,
                ).model_dump()
            ),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    @app.exception_handler(InvalidOperationException)
    async def invalid_operation_handler(
        request: Request, exc: InvalidOperationException
    ):
        return JSONResponse(
            content=(
                create_error_response(
                    status.HTTP_400_BAD_REQUEST,
                    exc.message,
                ).model_dump()
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(DomainException)
    async def general_domain_exception_handler(
        request: Request, exc: DomainException
    ):
        return JSONResponse(
            content=(
                create_error_response(
                    status.HTTP_400_BAD_REQUEST,
                    exc.message,
                ).model_dump()
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            content=(
                create_error_response(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "Internal Server Error",
                ).model_dump()
            ),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
