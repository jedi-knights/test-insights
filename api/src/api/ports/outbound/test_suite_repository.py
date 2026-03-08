from abc import ABC, abstractmethod

from api.domain.entities.test_suite import TestSuite


class TestSuiteRepository(ABC):
    @abstractmethod
    async def create(self, project_id: str, name: str, description: str | None) -> TestSuite: ...

    @abstractmethod
    async def find_by_id(self, suite_id: str) -> TestSuite | None: ...

    @abstractmethod
    async def find_by_project(self, project_id: str, skip: int = 0, limit: int = 100) -> list[TestSuite]: ...

    @abstractmethod
    async def update(self, suite_id: str, name: str | None, description: str | None) -> TestSuite | None: ...

    @abstractmethod
    async def delete(self, suite_id: str) -> bool: ...
