import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.adapters.outbound.persistence.models.project import ProjectModel
from api.domain.entities.project import Project
from api.ports.outbound.project_repository import ProjectRepository


def _to_entity(m: ProjectModel) -> Project:
    return Project(id=m.id, team_id=m.team_id, name=m.name, description=m.description, created_at=m.created_at, updated_at=m.updated_at)


class SqlProjectRepository(ProjectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, team_id: str, name: str, description: str | None) -> Project:
        now = datetime.now(timezone.utc)
        model = ProjectModel(id=str(uuid.uuid4()), team_id=team_id, name=name, description=description, created_at=now, updated_at=now)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_by_id(self, project_id: str) -> Project | None:
        result = await self._session.get(ProjectModel, project_id)
        return _to_entity(result) if result else None

    async def find_by_team(self, team_id: str, skip: int = 0, limit: int = 100) -> list[Project]:
        result = await self._session.execute(
            select(ProjectModel).where(ProjectModel.team_id == team_id).offset(skip).limit(limit)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, project_id: str, name: str | None, description: str | None) -> Project | None:
        model = await self._session.get(ProjectModel, project_id)
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

    async def delete(self, project_id: str) -> bool:
        model = await self._session.get(ProjectModel, project_id)
        if not model:
            return False
        await self._session.delete(model)
        await self._session.flush()
        return True
