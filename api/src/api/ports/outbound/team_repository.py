from abc import ABC, abstractmethod

from api.domain.entities.team import Team


class TeamRepository(ABC):
    @abstractmethod
    async def create(self, name: str, description: str | None) -> Team: ...

    @abstractmethod
    async def find_by_id(self, team_id: str) -> Team | None: ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> list[Team]: ...

    @abstractmethod
    async def update(self, team_id: str, name: str | None, description: str | None) -> Team | None: ...

    @abstractmethod
    async def delete(self, team_id: str) -> bool: ...
