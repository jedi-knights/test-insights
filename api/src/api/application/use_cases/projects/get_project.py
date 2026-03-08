from fastapi import HTTPException, status

from api.application.dto.project import ProjectResponse
from api.domain.entities.project import Project
from api.ports.outbound.project_repository import ProjectRepository


def _to_dto(p: Project) -> ProjectResponse:
    return ProjectResponse(id=p.id, team_id=p.team_id, name=p.name, description=p.description, created_at=p.created_at, updated_at=p.updated_at)


async def get_project(project_id: str, repo: ProjectRepository) -> ProjectResponse:
    project = await repo.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return _to_dto(project)
