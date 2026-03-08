from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass
class TeamModel:
    id: str
    name: str
    description: str | None = None


@dataclass
class ProjectModel:
    id: str
    team_id: str
    name: str
    description: str | None = None


@dataclass
class SuiteModel:
    id: str
    project_id: str
    name: str
    description: str | None = None


@dataclass
class RunModel:
    id: str
    suite_id: str
    status: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    metadata: dict = field(default_factory=dict)
