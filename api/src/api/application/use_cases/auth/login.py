from fastapi import HTTPException, status

from api.application.dto.auth import LoginRequest, TokenResponse
from api.infrastructure.security import create_access_token, create_refresh_token, verify_password
from api.ports.outbound.user_repository import UserRepository


async def login(request: LoginRequest, users: UserRepository) -> TokenResponse:
    user = await users.find_by_email(request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")
    access_token = create_access_token(user.id)
    refresh_token, _ = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
