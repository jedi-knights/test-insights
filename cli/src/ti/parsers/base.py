from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ParsedCase:
    name: str
    status: str  # passed | failed | error | skipped
    classname: str | None = None
    file_path: str | None = None
    duration_seconds: float | None = None
    error_message: str | None = None
    stack_trace: str | None = None


@dataclass
class ParsedRun:
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    error_tests: int
    duration_seconds: float | None
    started_at: datetime | None
    cases: list[ParsedCase] = field(default_factory=list)
