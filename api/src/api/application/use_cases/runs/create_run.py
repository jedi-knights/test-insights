from fastapi import HTTPException, status

from api.application.dto.test_run import TestRunCreate, TestRunResponse
from api.domain.entities.test_run import TestRun
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository


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


async def create_run(suite_id: str, request: TestRunCreate, suites: TestSuiteRepository, repo: TestRunRepository) -> TestRunResponse:
    suite = await suites.find_by_id(suite_id)
    if not suite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suite not found")
    run = await repo.create(
        suite_id=suite_id,
        build_system=request.build_system,
        branch=request.branch,
        commit_sha=request.commit_sha,
        status=request.status,
        total_tests=request.total_tests,
        passed_tests=request.passed_tests,
        failed_tests=request.failed_tests,
        skipped_tests=request.skipped_tests,
        error_tests=request.error_tests,
        duration_seconds=request.duration_seconds,
        started_at=request.started_at,
        completed_at=request.completed_at,
        metadata=request.metadata,
    )
    return _to_dto(run)
