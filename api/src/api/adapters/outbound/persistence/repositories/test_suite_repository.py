import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.adapters.outbound.persistence.models.test_suite import TestSuiteModel
from api.domain.entities.test_suite import TestSuite
from api.ports.outbound.test_suite_repository import TestSuiteRepository


def _to_entity(m: TestSuiteModel) -> TestSuite:
    return TestSuite(id=m.id, project_id=m.project_id, name=m.name, description=m.description, created_at=m.created_at, updated_at=m.updated_at)


class SqlTestSuiteRepository(TestSuiteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, project_id: str, name: str, description: str | None) -> TestSuite:
        now = datetime.now(timezone.utc)
        model = TestSuiteModel(id=str(uuid.uuid4()), project_id=project_id, name=name, description=description, created_at=now, updated_at=now)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_by_id(self, suite_id: str) -> TestSuite | None:
        result = await self._session.get(TestSuiteModel, suite_id)
        return _to_entity(result) if result else None

    async def find_by_project(self, project_id: str, skip: int = 0, limit: int = 100) -> list[TestSuite]:
        result = await self._session.execute(
            select(TestSuiteModel).where(TestSuiteModel.project_id == project_id).offset(skip).limit(limit)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, suite_id: str, name: str | None, description: str | None) -> TestSuite | None:
        model = await self._session.get(TestSuiteModel, suite_id)
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

    async def delete(self, suite_id: str) -> bool:
        model = await self._session.get(TestSuiteModel, suite_id)
        if not model:
            return False
        await self._session.delete(model)
        await self._session.flush()
        return True
