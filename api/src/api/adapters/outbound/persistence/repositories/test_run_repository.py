import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from api.adapters.outbound.persistence.models.test_run import TestRunModel
from api.domain.entities.test_run import BuildSystem, RunStatus, TestRun
from api.ports.outbound.test_run_repository import PassRatePoint, TestRunRepository


def _to_entity(m: TestRunModel) -> TestRun:
    return TestRun(
        id=m.id,
        suite_id=m.suite_id,
        build_system=BuildSystem(m.build_system),
        branch=m.branch,
        commit_sha=m.commit_sha,
        status=RunStatus(m.status),
        total_tests=m.total_tests,
        passed_tests=m.passed_tests,
        failed_tests=m.failed_tests,
        skipped_tests=m.skipped_tests,
        error_tests=m.error_tests,
        duration_seconds=m.duration_seconds,
        started_at=m.started_at,
        completed_at=m.completed_at,
        created_at=m.created_at,
        metadata=m.metadata_ or {},
    )


class SqlTestRunRepository(TestRunRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

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
    ) -> TestRun:
        model = TestRunModel(
            id=str(uuid.uuid4()),
            suite_id=suite_id,
            build_system=build_system.value,
            branch=branch,
            commit_sha=commit_sha,
            status=status.value,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            skipped_tests=skipped_tests,
            error_tests=error_tests,
            duration_seconds=duration_seconds,
            started_at=started_at,
            completed_at=completed_at,
            created_at=datetime.now(timezone.utc),
            metadata_=metadata,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_by_id(self, run_id: str) -> TestRun | None:
        result = await self._session.get(TestRunModel, run_id)
        return _to_entity(result) if result else None

    async def find_by_suite(self, suite_id: str, skip: int = 0, limit: int = 100) -> list[TestRun]:
        result = await self._session.execute(
            select(TestRunModel)
            .where(TestRunModel.suite_id == suite_id)
            .order_by(TestRunModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def find_pass_rate_trend(self, suite_id: str, limit: int = 30) -> list[PassRatePoint]:
        stmt = text("""
            SELECT
                DATE(started_at AT TIME ZONE 'UTC') as run_date,
                SUM(passed_tests)::float / NULLIF(SUM(total_tests), 0) as pass_rate,
                SUM(total_tests)::int as total
            FROM test_runs
            WHERE suite_id = :suite_id
              AND started_at IS NOT NULL
            GROUP BY run_date
            ORDER BY run_date DESC
            LIMIT :limit
        """)
        result = await self._session.execute(stmt, {"suite_id": suite_id, "limit": limit})
        rows = result.fetchall()
        return [
            PassRatePoint(date=str(row.run_date), pass_rate=float(row.pass_rate or 0.0), total=int(row.total or 0))
            for row in reversed(rows)
        ]
