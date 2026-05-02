from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class ModuleStatus(BaseModel):
    status: str = "placeholder"
    module: str
    detail: str
