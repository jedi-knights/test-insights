from api.application.dto.team import TeamResponse
from api.domain.entities.team import Team
from api.ports.outbound.team_repository import TeamRepository


def _to_dto(t: Team) -> TeamResponse:
    return TeamResponse(id=t.id, name=t.name, description=t.description, created_at=t.created_at, updated_at=t.updated_at)


async def list_teams(repo: TeamRepository, skip: int = 0, limit: int = 100) -> list[TeamResponse]:
    teams = await repo.find_all(skip=skip, limit=limit)
    return [_to_dto(t) for t in teams]
