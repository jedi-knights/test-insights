import logging

from api.adapters.outbound.persistence.database import AsyncSessionLocal
from api.adapters.outbound.persistence.repositories.user_repository import SqlUserRepository
from api.infrastructure.config import settings
from api.infrastructure.security import hash_password

logger = logging.getLogger(__name__)


async def provision_admin() -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            repo = SqlUserRepository(session)
            existing = await repo.find_by_email(settings.admin_email)
            if existing:
                return
            await repo.create(settings.admin_email, hash_password(settings.admin_password), settings.admin_full_name)
            logger.info("Admin user provisioned: %s", settings.admin_email)
