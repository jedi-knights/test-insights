from fastapi import HTTPException, status

from api.application.dto.test_suite import TestSuiteResponse
from api.domain.entities.test_suite import TestSuite
from api.ports.outbound.test_suite_repository import TestSuiteRepository


def _to_dto(s: TestSuite) -> TestSuiteResponse:
    return TestSuiteResponse(id=s.id, project_id=s.project_id, name=s.name, description=s.description, created_at=s.created_at, updated_at=s.updated_at)


async def get_suite(suite_id: str, repo: TestSuiteRepository) -> TestSuiteResponse:
    suite = await repo.find_by_id(suite_id)
    if not suite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suite not found")
    return _to_dto(suite)
