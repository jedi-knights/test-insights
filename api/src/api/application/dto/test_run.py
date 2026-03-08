from datetime import datetime

from pydantic import BaseModel

from api.domain.entities.test_run import BuildSystem, RunStatus


class TestRunCreate(BaseModel):
    build_system: BuildSystem = BuildSystem.UNKNOWN
    branch: str | None = None
    commit_sha: str | None = None
    status: RunStatus = RunStatus.RUNNING
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    error_tests: int = 0
    duration_seconds: float | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    metadata: dict = {}


class TestRunResponse(BaseModel):
    id: str
    suite_id: str
    build_system: BuildSystem
    branch: str | None
    commit_sha: str | None
    status: RunStatus
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    error_tests: int
    duration_seconds: float | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    metadata: dict
