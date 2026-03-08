from fastapi import HTTPException, status

from api.application.dto.project import ProjectResponse, ProjectUpdate
from api.domain.entities.project import Project
from api.ports.outbound.project_repository import ProjectRepository


def _to_dto(p: Project) -> ProjectResponse:
    return ProjectResponse(id=p.id, team_id=p.team_id, name=p.name, description=p.description, created_at=p.created_at, updated_at=p.updated_at)


async def update_project(project_id: str, request: ProjectUpdate, repo: ProjectRepository) -> ProjectResponse:
    project = await repo.update(project_id, name=request.name, description=request.description)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return _to_dto(project)
