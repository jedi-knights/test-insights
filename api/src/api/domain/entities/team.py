from dataclasses import dataclass
from datetime import datetime


@dataclass
class Team:
    id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
