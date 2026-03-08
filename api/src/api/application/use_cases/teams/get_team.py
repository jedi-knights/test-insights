from fastapi import HTTPException, status

from api.application.dto.team import TeamResponse
from api.domain.entities.team import Team
from api.ports.outbound.team_repository import TeamRepository


def _to_dto(t: Team) -> TeamResponse:
    return TeamResponse(id=t.id, name=t.name, description=t.description, created_at=t.created_at, updated_at=t.updated_at)


async def get_team(team_id: str, repo: TeamRepository) -> TeamResponse:
    team = await repo.find_by_id(team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return _to_dto(team)
