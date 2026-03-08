from api.application.dto.project import ProjectResponse
from api.domain.entities.project import Project
from api.ports.outbound.project_repository import ProjectRepository


def _to_dto(p: Project) -> ProjectResponse:
    return ProjectResponse(id=p.id, team_id=p.team_id, name=p.name, description=p.description, created_at=p.created_at, updated_at=p.updated_at)


async def list_projects(team_id: str, repo: ProjectRepository, skip: int = 0, limit: int = 100) -> list[ProjectResponse]:
    projects = await repo.find_by_team(team_id, skip=skip, limit=limit)
    return [_to_dto(p) for p in projects]
