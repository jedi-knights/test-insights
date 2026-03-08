from fastapi import HTTPException, status

from api.application.dto.project import ProjectCreate, ProjectResponse
from api.domain.entities.project import Project
from api.ports.outbound.project_repository import ProjectRepository
from api.ports.outbound.team_repository import TeamRepository


def _to_dto(p: Project) -> ProjectResponse:
    return ProjectResponse(id=p.id, team_id=p.team_id, name=p.name, description=p.description, created_at=p.created_at, updated_at=p.updated_at)


async def create_project(team_id: str, request: ProjectCreate, teams: TeamRepository, projects: ProjectRepository) -> ProjectResponse:
    team = await teams.find_by_id(team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    project = await projects.create(team_id=team_id, name=request.name, description=request.description)
    return _to_dto(project)
