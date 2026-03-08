import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.adapters.outbound.persistence.models.user import UserModel
from api.domain.entities.user import User
from api.ports.outbound.user_repository import UserRepository


def _to_entity(m: UserModel) -> User:
    return User(
        id=m.id,
        email=m.email,
        hashed_password=m.hashed_password,
        full_name=m.full_name,
        is_active=m.is_active,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


class SqlUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, email: str, hashed_password: str, full_name: str | None) -> User:
        now = datetime.now(timezone.utc)
        model = UserModel(
            id=str(uuid.uuid4()),
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def find_by_id(self, user_id: str) -> User | None:
        result = await self._session.get(UserModel, user_id)
        return _to_entity(result) if result else None

    async def find_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None
