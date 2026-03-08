from datetime import datetime

from pydantic import BaseModel

from api.domain.entities.test_case import CaseStatus


class TestCaseCreate(BaseModel):
    name: str
    classname: str | None = None
    file_path: str | None = None
    status: CaseStatus
    duration_seconds: float | None = None
    error_message: str | None = None
    stack_trace: str | None = None


class TestCaseResponse(BaseModel):
    id: str
    run_id: str
    name: str
    classname: str | None
    file_path: str | None
    status: CaseStatus
    duration_seconds: float | None
    error_message: str | None
    stack_trace: str | None
    created_at: datetime


class BulkCaseCreate(BaseModel):
    cases: list[TestCaseCreate]
