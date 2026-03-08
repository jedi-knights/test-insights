from fastapi import HTTPException, status

from api.application.dto.auth import TokenResponse
from api.infrastructure.security import create_access_token, create_refresh_token, decode_token_safe
from api.ports.outbound.token_repository import TokenRepository


async def refresh_token(refresh_token_str: str, tokens: TokenRepository) -> TokenResponse:
    payload = decode_token_safe(refresh_token_str)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    jti = payload.get("jti")
    if jti and await tokens.is_blocklisted(jti):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # Blocklist old jti (single-use rotation)
    if jti:
        await tokens.blocklist_jti(jti)
    access_token = create_access_token(user_id)
    new_refresh_token, _ = create_refresh_token(user_id)
    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)
