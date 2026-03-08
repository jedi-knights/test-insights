from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class CaseStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class TestCase:
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
