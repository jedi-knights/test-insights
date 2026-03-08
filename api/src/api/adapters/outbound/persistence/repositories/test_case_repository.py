import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.adapters.outbound.persistence.models.test_case import TestCaseModel
from api.domain.entities.test_case import CaseStatus, TestCase
from api.ports.outbound.test_case_repository import TestCaseRepository


def _to_entity(m: TestCaseModel) -> TestCase:
    return TestCase(
        id=m.id,
        run_id=m.run_id,
        name=m.name,
        classname=m.classname,
        file_path=m.file_path,
        status=CaseStatus(m.status),
        duration_seconds=m.duration_seconds,
        error_message=m.error_message,
        stack_trace=m.stack_trace,
        created_at=m.created_at,
    )


class SqlTestCaseRepository(TestCaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def bulk_create(self, run_id: str, cases: list[dict]) -> list[TestCase]:
        now = datetime.now(timezone.utc)
        models = [
            TestCaseModel(
                id=str(uuid.uuid4()),
                run_id=run_id,
                name=c["name"],
                classname=c.get("classname"),
                file_path=c.get("file_path"),
                status=c["status"],
                duration_seconds=c.get("duration_seconds"),
                error_message=c.get("error_message"),
                stack_trace=c.get("stack_trace"),
                created_at=now,
            )
            for c in cases
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [_to_entity(m) for m in models]

    async def find_by_run(self, run_id: str) -> list[TestCase]:
        result = await self._session.execute(
            select(TestCaseModel).where(TestCaseModel.run_id == run_id)
        )
        return [_to_entity(m) for m in result.scalars().all()]
