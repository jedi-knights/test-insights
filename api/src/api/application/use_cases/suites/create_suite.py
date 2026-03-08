from fastapi import HTTPException, status

from api.application.dto.test_suite import TestSuiteCreate, TestSuiteResponse
from api.domain.entities.test_suite import TestSuite
from api.ports.outbound.project_repository import ProjectRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository


def _to_dto(s: TestSuite) -> TestSuiteResponse:
    return TestSuiteResponse(id=s.id, project_id=s.project_id, name=s.name, description=s.description, created_at=s.created_at, updated_at=s.updated_at)


async def create_suite(project_id: str, request: TestSuiteCreate, projects: ProjectRepository, repo: TestSuiteRepository) -> TestSuiteResponse:
    project = await projects.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    suite = await repo.create(project_id=project_id, name=request.name, description=request.description)
    return _to_dto(suite)
