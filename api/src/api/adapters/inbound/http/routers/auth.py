from typing import Annotated

from fastapi import APIRouter, Depends

from api.adapters.inbound.http.dependencies import get_current_user, get_token_repo, get_user_repo
from api.application.dto.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse, UserResponse
from api.application.use_cases.auth import login as login_uc
from api.application.use_cases.auth import logout as logout_uc
from api.application.use_cases.auth import refresh_token as refresh_uc
from api.application.use_cases.auth import register as register_uc
from api.domain.entities.user import User
from api.ports.outbound.token_repository import TokenRepository
from api.ports.outbound.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    request: RegisterRequest,
    users: Annotated[UserRepository, Depends(get_user_repo)],
) -> TokenResponse:
    return await register_uc.register(request, users)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    users: Annotated[UserRepository, Depends(get_user_repo)],
) -> TokenResponse:
    return await login_uc.login(request, users)


@router.post("/logout", status_code=204)
async def logout(
    request: RefreshRequest,
    tokens: Annotated[TokenRepository, Depends(get_token_repo)],
) -> None:
    await logout_uc.logout(request.refresh_token, tokens)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: RefreshRequest,
    tokens: Annotated[TokenRepository, Depends(get_token_repo)],
) -> TokenResponse:
    return await refresh_uc.refresh_token(request.refresh_token, tokens)


@router.get("/me", response_model=UserResponse)
async def me(current_user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
    )
