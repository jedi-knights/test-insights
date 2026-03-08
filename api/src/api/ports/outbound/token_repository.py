from abc import ABC, abstractmethod


class TokenRepository(ABC):
    @abstractmethod
    async def blocklist_jti(self, jti: str) -> None: ...

    @abstractmethod
    async def is_blocklisted(self, jti: str) -> bool: ...
