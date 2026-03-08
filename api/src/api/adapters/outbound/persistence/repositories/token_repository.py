from api.ports.outbound.token_repository import TokenRepository


class InMemoryTokenRepository(TokenRepository):
    """Single-process in-memory blocklist. Replace with Redis for multi-instance deployments."""

    def __init__(self) -> None:
        self._blocklist: set[str] = set()

    async def blocklist_jti(self, jti: str) -> None:
        self._blocklist.add(jti)

    async def is_blocklisted(self, jti: str) -> bool:
        return jti in self._blocklist
