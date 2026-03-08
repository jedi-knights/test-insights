from fastapi import HTTPException, status

from api.application.dto.test_case import BulkCaseCreate, TestCaseResponse
from api.ports.outbound.test_case_repository import TestCaseRepository
from api.ports.outbound.test_run_repository import TestRunRepository


async def bulk_create_cases(run_id: str, request: BulkCaseCreate, runs: TestRunRepository, cases: TestCaseRepository) -> list[TestCaseResponse]:
    run = await runs.find_by_id(run_id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    case_dicts = [c.model_dump() for c in request.cases]
    created = await cases.bulk_create(run_id=run_id, cases=case_dicts)
    return [
        TestCaseResponse(
            id=c.id, run_id=c.run_id, name=c.name, classname=c.classname,
            file_path=c.file_path, status=c.status, duration_seconds=c.duration_seconds,
            error_message=c.error_message, stack_trace=c.stack_trace, created_at=c.created_at,
        )
        for c in created
    ]
