from fastapi import HTTPException, status

from api.application.dto.team import TeamResponse, TeamUpdate
from api.domain.entities.team import Team
from api.ports.outbound.team_repository import TeamRepository


def _to_dto(t: Team) -> TeamResponse:
    return TeamResponse(id=t.id, name=t.name, description=t.description, created_at=t.created_at, updated_at=t.updated_at)


async def update_team(team_id: str, request: TeamUpdate, repo: TeamRepository) -> TeamResponse:
    team = await repo.update(team_id, name=request.name, description=request.description)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return _to_dto(team)
