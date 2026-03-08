from fastapi import HTTPException, status

from api.application.dto.auth import RegisterRequest, TokenResponse
from api.infrastructure.security import create_access_token, create_refresh_token, hash_password
from api.ports.outbound.user_repository import UserRepository


async def register(request: RegisterRequest, users: UserRepository) -> TokenResponse:
    existing = await users.find_by_email(request.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    hashed = hash_password(request.password)
    user = await users.create(request.email, hashed, request.full_name)
    access_token = create_access_token(user.id)
    refresh_token, _ = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
