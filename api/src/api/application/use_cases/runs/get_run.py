from fastapi import HTTPException, status

from api.application.dto.test_case import TestCaseResponse
from api.application.dto.test_run import TestRunResponse
from api.domain.entities.test_run import TestRun
from api.ports.outbound.test_case_repository import TestCaseRepository
from api.ports.outbound.test_run_repository import TestRunRepository
from pydantic import BaseModel


class RunDetail(BaseModel):
    run: TestRunResponse
    cases: list[TestCaseResponse]


def _run_to_dto(r: TestRun) -> TestRunResponse:
    return TestRunResponse(
        id=r.id, suite_id=r.suite_id, build_system=r.build_system,
        branch=r.branch, commit_sha=r.commit_sha, status=r.status,
        total_tests=r.total_tests, passed_tests=r.passed_tests,
        failed_tests=r.failed_tests, skipped_tests=r.skipped_tests,
        error_tests=r.error_tests, duration_seconds=r.duration_seconds,
        started_at=r.started_at, completed_at=r.completed_at,
        created_at=r.created_at, metadata=r.metadata,
    )


async def get_run(run_id: str, runs: TestRunRepository, cases: TestCaseRepository) -> RunDetail:
    run = await runs.find_by_id(run_id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
    run_cases = await cases.find_by_run(run_id)
    case_dtos = [
        TestCaseResponse(
            id=c.id, run_id=c.run_id, name=c.name, classname=c.classname,
            file_path=c.file_path, status=c.status, duration_seconds=c.duration_seconds,
            error_message=c.error_message, stack_trace=c.stack_trace, created_at=c.created_at,
        )
        for c in run_cases
    ]
    return RunDetail(run=_run_to_dto(run), cases=case_dtos)
