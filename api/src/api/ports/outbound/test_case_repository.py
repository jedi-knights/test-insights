from abc import ABC, abstractmethod

from api.domain.entities.test_case import CaseStatus, TestCase


class TestCaseRepository(ABC):
    @abstractmethod
    async def bulk_create(
        self,
        run_id: str,
        cases: list[dict],
    ) -> list[TestCase]: ...

    @abstractmethod
    async def find_by_run(self, run_id: str) -> list[TestCase]: ...
