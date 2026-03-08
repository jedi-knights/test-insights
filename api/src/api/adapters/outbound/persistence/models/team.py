from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from api.adapters.outbound.persistence.models.base import Base, TimestampMixin


class TeamModel(Base, TimestampMixin):
    __tablename__ = "teams"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
