from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.adapters.outbound.persistence.database import get_db
from api.adapters.outbound.persistence.repositories.project_repository import SqlProjectRepository
from api.adapters.outbound.persistence.repositories.team_repository import SqlTeamRepository
from api.adapters.outbound.persistence.repositories.test_case_repository import SqlTestCaseRepository
from api.adapters.outbound.persistence.repositories.test_run_repository import SqlTestRunRepository
from api.adapters.outbound.persistence.repositories.test_suite_repository import SqlTestSuiteRepository
from api.adapters.outbound.persistence.repositories.token_repository import InMemoryTokenRepository
from api.adapters.outbound.persistence.repositories.user_repository import SqlUserRepository
from api.domain.entities.user import User
from api.infrastructure.security import decode_token_safe
from api.ports.outbound.project_repository import ProjectRepository
from api.ports.outbound.team_repository import TeamRepository
from api.ports.outbound.test_case_repository import TestCaseRepository
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository
from api.ports.outbound.token_repository import TokenRepository
from api.ports.outbound.user_repository import UserRepository

# Singleton token repository (in-memory)
_token_repo = InMemoryTokenRepository()

bearer_scheme = HTTPBearer(auto_error=False)


def get_token_repo() -> TokenRepository:
    return _token_repo


async def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return SqlUserRepository(db)


async def get_team_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> TeamRepository:
    return SqlTeamRepository(db)


async def get_project_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> ProjectRepository:
    return SqlProjectRepository(db)


async def get_suite_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> TestSuiteRepository:
    return SqlTestSuiteRepository(db)


async def get_run_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> TestRunRepository:
    return SqlTestRunRepository(db)


async def get_case_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> TestCaseRepository:
    return SqlTestCaseRepository(db)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    users: Annotated[UserRepository, Depends(get_user_repo)],
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_token_safe(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await users.find_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
