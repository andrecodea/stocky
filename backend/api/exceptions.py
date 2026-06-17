"""Application-level exceptions and global error handlers."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Recurso", identifier: str = "") -> None:
        detail = f"{resource} não encontrado"
        if identifier:
            detail = f"{resource} '{identifier}' não encontrado"
        self.detail = detail
        super().__init__(self.detail)


class ForbiddenError(Exception):
    """Raised when the user lacks permission for the operation."""

    def __init__(self, detail: str = "Acesso negado") -> None:
        self.detail = detail
        super().__init__(self.detail)


class ConflictError(Exception):
    """Raised on uniqueness violations or conflicting state."""

    def __init__(self, detail: str = "Conflito de dados") -> None:
        self.detail = detail
        super().__init__(self.detail)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI application."""

    @app.exception_handler(NotFoundError)
    async def _not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @app.exception_handler(ForbiddenError)
    async def _forbidden_handler(
        request: Request, exc: ForbiddenError
    ) -> JSONResponse:
        return JSONResponse(status_code=403, content={"detail": exc.detail})

    @app.exception_handler(ConflictError)
    async def _conflict_handler(
        request: Request, exc: ConflictError
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.detail})
