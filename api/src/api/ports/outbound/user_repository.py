from abc import ABC, abstractmethod

from api.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, email: str, hashed_password: str, full_name: str | None) -> User: ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...
