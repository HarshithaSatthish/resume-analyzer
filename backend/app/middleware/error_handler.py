from fastapi import HTTPException, status


class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication failed."):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(AppException):
    def __init__(self, message: str = "You do not have permission to access this resource."):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found."):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class ValidationError(AppException):
    def __init__(self, message: str = "Validation failed."):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def register_exception_handlers(app) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_, exc: AppException):
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException):
        from fastapi.responses import JSONResponse

        detail = exc.detail
        if isinstance(detail, dict):
            message = detail.get("message", "Request failed.")
        elif isinstance(detail, list):
            message = "; ".join(str(item) for item in detail)
        else:
            message = str(detail)

        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": message},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_, exc: Exception):
        from fastapi.responses import JSONResponse

        from app.config import settings

        message = str(exc) if settings.debug else "An unexpected error occurred."
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": message},
        )
