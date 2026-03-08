from api.application.dto.test_suite import TestSuiteResponse
from api.domain.entities.test_suite import TestSuite
from api.ports.outbound.test_suite_repository import TestSuiteRepository


def _to_dto(s: TestSuite) -> TestSuiteResponse:
    return TestSuiteResponse(id=s.id, project_id=s.project_id, name=s.name, description=s.description, created_at=s.created_at, updated_at=s.updated_at)


async def list_suites(project_id: str, repo: TestSuiteRepository, skip: int = 0, limit: int = 100) -> list[TestSuiteResponse]:
    suites = await repo.find_by_project(project_id, skip=skip, limit=limit)
    return [_to_dto(s) for s in suites]
