from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class BuildSystem(StrEnum):
    GITHUB_ACTIONS = "github_actions"
    GITLAB_CI = "gitlab_ci"
    JENKINS = "jenkins"
    CIRCLECI = "circleci"
    LOCAL = "local"
    UNKNOWN = "unknown"


class RunStatus(StrEnum):
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


@dataclass
class TestRun:
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
    metadata: dict = field(default_factory=dict)
