from fastapi import HTTPException, status

from api.ports.outbound.team_repository import TeamRepository


async def delete_team(team_id: str, repo: TeamRepository) -> None:
    deleted = await repo.delete(team_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
