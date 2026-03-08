from api.application.dto.team import TeamCreate, TeamResponse
from api.domain.entities.team import Team
from api.ports.outbound.team_repository import TeamRepository


def _to_dto(t: Team) -> TeamResponse:
    return TeamResponse(id=t.id, name=t.name, description=t.description, created_at=t.created_at, updated_at=t.updated_at)


async def create_team(request: TeamCreate, repo: TeamRepository) -> TeamResponse:
    team = await repo.create(name=request.name, description=request.description)
    return _to_dto(team)
