import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.adapters.outbound.persistence.models.team import TeamModel
from api.domain.entities.team import Team
from api.ports.outbound.team_repository import TeamRepository


def _to_entity(m: TeamModel) -> Team:
    return Team(id=m.id, name=m.name, description=m.description, created_at=m.created_at, updated_at=m.updated_at)


class SqlTeamRepository(TeamRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, name: str, description: str | None) -> Team:
        now = datetime.now(timezone.utc)
        model = TeamModel(id=str(uuid.uuid4()), name=name, description=description, created_at=now, updated_at=now)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_by_id(self, team_id: str) -> Team | None:
        result = await self._session.get(TeamModel, team_id)
        return _to_entity(result) if result else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> list[Team]:
        result = await self._session.execute(select(TeamModel).offset(skip).limit(limit))
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, team_id: str, name: str | None, description: str | None) -> Team | None:
        model = await self._session.get(TeamModel, team_id)
        if not model:
            return None
        if name is not None:
            model.name = name
        if description is not None:
            model.description = description
        model.updated_at = datetime.now(timezone.utc)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def delete(self, team_id: str) -> bool:
        model = await self._session.get(TeamModel, team_id)
        if not model:
            return False
        await self._session.delete(model)
        await self._session.flush()
        return True
