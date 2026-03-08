from datetime import datetime

from pydantic import BaseModel


class TestSuiteCreate(BaseModel):
    name: str
    description: str | None = None


class TestSuiteUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class TestSuiteResponse(BaseModel):
    id: str
    project_id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
