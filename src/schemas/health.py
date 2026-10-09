from pydantic import BaseModel


class HealthResponse(BaseModel):
    app_name: str
    status: str
    version: str
    environment: str
