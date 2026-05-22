from fastapi import Request, FastAPI

from fastapi.responses import JSONResponse
from jose import JWTError

from src.utils.exceptions.exceptions import (
    NotFound,
    ProductAlreadyExists,
    NotAuthorized,
    PermissionDeniedError,
    EmailAlreadyExists,
    InvalidCredentials,
    UserNotFound,
)
from src.services.log_service import log_service


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFound)
    async def product_not_found_handler(
        request: Request,
        exc: NotFound,
    ):
        """Global NotFound exception handler."""
        log_service.error(
            status_code=404, message=f"product not found{request.path_params}"
        )
        return JSONResponse(
            status_code=404,
            content={"detail": "Product not found"},
        )

    @app.exception_handler(ProductAlreadyExists)
    async def product_already_exists_handler(
        request: Request,
        exc: ProductAlreadyExists,
    ):
        log_service.error(
            status_code=400,
            message=f"product already exists {request.query_params}",
        )
        return JSONResponse(
            status_code=400, content={"detail": "Product already exists"}
        )

    @app.exception_handler(NotAuthorized)
    async def jwt_error_handler(
        request: Request,
        exc: NotAuthorized,
    ):
        log_service.error(status_code=401, message=str(exc))
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(PermissionDeniedError)
    async def permission_error_handler(
        request: Request,
        exc: PermissionDeniedError,
    ):
        log_service.error(status_code=403, message=str(exc))
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(EmailAlreadyExists)
    async def email_already_exists_handler(
        request: Request,
        exc: EmailAlreadyExists,
    ):
        log_service.error(status_code=400, message=str(exc))
        return JSONResponse(
            status_code=400, content={"detail": "Email already registered"}
        )

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentials,
    ):
        log_service.error(status_code=401, message=str(exc))
        return JSONResponse(
            status_code=401, content={"detail": "Invalid credentials"}
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFound,
    ):
        log_service.error(status_code=404, message=str(exc))
        return JSONResponse(
            status_code=404, content={"detail": "User not found"}
        )
