from api.application.dto.test_run import TestRunResponse
from api.domain.entities.test_run import TestRun
from api.ports.outbound.test_run_repository import TestRunRepository


def _to_dto(r: TestRun) -> TestRunResponse:
    return TestRunResponse(
        id=r.id, suite_id=r.suite_id, build_system=r.build_system,
        branch=r.branch, commit_sha=r.commit_sha, status=r.status,
        total_tests=r.total_tests, passed_tests=r.passed_tests,
        failed_tests=r.failed_tests, skipped_tests=r.skipped_tests,
        error_tests=r.error_tests, duration_seconds=r.duration_seconds,
        started_at=r.started_at, completed_at=r.completed_at,
        created_at=r.created_at, metadata=r.metadata,
    )


async def list_runs(suite_id: str, repo: TestRunRepository, skip: int = 0, limit: int = 100) -> list[TestRunResponse]:
    runs = await repo.find_by_suite(suite_id, skip=skip, limit=limit)
    return [_to_dto(r) for r in runs]
