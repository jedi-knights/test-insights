from abc import ABC, abstractmethod

from api.domain.entities.project import Project


class ProjectRepository(ABC):
    @abstractmethod
    async def create(self, team_id: str, name: str, description: str | None) -> Project: ...

    @abstractmethod
    async def find_by_id(self, project_id: str) -> Project | None: ...

    @abstractmethod
    async def find_by_team(self, team_id: str, skip: int = 0, limit: int = 100) -> list[Project]: ...

    @abstractmethod
    async def update(self, project_id: str, name: str | None, description: str | None) -> Project | None: ...

    @abstractmethod
    async def delete(self, project_id: str) -> bool: ...
