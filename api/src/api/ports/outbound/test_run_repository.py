from abc import ABC, abstractmethod
from datetime import datetime

from api.domain.entities.test_run import BuildSystem, RunStatus, TestRun


class PassRatePoint:
    def __init__(self, date: str, pass_rate: float, total: int) -> None:
        self.date = date
        self.pass_rate = pass_rate
        self.total = total


class TestRunRepository(ABC):
    @abstractmethod
    async def create(
        self,
        suite_id: str,
        build_system: BuildSystem,
        branch: str | None,
        commit_sha: str | None,
        status: RunStatus,
        total_tests: int,
        passed_tests: int,
        failed_tests: int,
        skipped_tests: int,
        error_tests: int,
        duration_seconds: float | None,
        started_at: datetime | None,
        completed_at: datetime | None,
        metadata: dict,
    ) -> TestRun: ...

    @abstractmethod
    async def find_by_id(self, run_id: str) -> TestRun | None: ...

    @abstractmethod
    async def find_by_suite(self, suite_id: str, skip: int = 0, limit: int = 100) -> list[TestRun]: ...

    @abstractmethod
    async def find_pass_rate_trend(self, suite_id: str, limit: int = 30) -> list[PassRatePoint]: ...
