from pydantic import BaseModel


class MessageResponse(BaseModel):
    success: bool = True
    message: str


class DatabaseHealth(BaseModel):
    status: str
    connected: bool
    detail: str | None = None
    database: str | None = None
    collections: int | None = None
    documents: int | None = None


class HealthResponse(BaseModel):
    status: str
    app_name: str
    environment: str
    database: DatabaseHealth
