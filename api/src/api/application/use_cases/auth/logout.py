from fastapi import HTTPException, status

from api.infrastructure.security import decode_token_safe
from api.ports.outbound.token_repository import TokenRepository


async def logout(refresh_token: str, tokens: TokenRepository) -> None:
    payload = decode_token_safe(refresh_token)
    if payload and payload.get("type") == "refresh":
        jti = payload.get("jti")
        if jti:
            await tokens.blocklist_jti(jti)
