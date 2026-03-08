from typing import Annotated

from fastapi import APIRouter, Depends

from api.adapters.inbound.http.dependencies import (
    get_current_user,
    get_project_repo,
    get_run_repo,
    get_suite_repo,
    get_team_repo,
)
from api.application.dto.metrics import TeamMetrics
from api.application.dto.team import TeamCreate, TeamResponse, TeamUpdate
from api.application.use_cases.teams import (
    create_team,
    delete_team,
    get_team,
    list_teams,
    metrics as team_metrics,
    update_team,
)
from api.domain.entities.user import User
from api.ports.outbound.project_repository import ProjectRepository
from api.ports.outbound.team_repository import TeamRepository
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository

router = APIRouter(prefix="/teams", tags=["teams"])
Auth = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[TeamResponse])
async def list_(
    _: Auth,
    repo: Annotated[TeamRepository, Depends(get_team_repo)],
    skip: int = 0,
    limit: int = 100,
) -> list[TeamResponse]:
    return await list_teams.list_teams(repo, skip=skip, limit=limit)


@router.post("", response_model=TeamResponse, status_code=201)
async def create(
    _: Auth,
    request: TeamCreate,
    repo: Annotated[TeamRepository, Depends(get_team_repo)],
) -> TeamResponse:
    return await create_team.create_team(request, repo)


@router.get("/{team_id}", response_model=TeamResponse)
async def get(
    _: Auth,
    team_id: str,
    repo: Annotated[TeamRepository, Depends(get_team_repo)],
) -> TeamResponse:
    return await get_team.get_team(team_id, repo)


@router.put("/{team_id}", response_model=TeamResponse)
async def update(
    _: Auth,
    team_id: str,
    request: TeamUpdate,
    repo: Annotated[TeamRepository, Depends(get_team_repo)],
) -> TeamResponse:
    return await update_team.update_team(team_id, request, repo)


@router.delete("/{team_id}", status_code=204)
async def delete(
    _: Auth,
    team_id: str,
    repo: Annotated[TeamRepository, Depends(get_team_repo)],
) -> None:
    await delete_team.delete_team(team_id, repo)


@router.get("/{team_id}/metrics", response_model=TeamMetrics)
async def get_metrics(
    _: Auth,
    team_id: str,
    teams: Annotated[TeamRepository, Depends(get_team_repo)],
    projects: Annotated[ProjectRepository, Depends(get_project_repo)],
    suites: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
    runs: Annotated[TestRunRepository, Depends(get_run_repo)],
) -> TeamMetrics:
    return await team_metrics.get_team_metrics(team_id, teams, projects, suites, runs)
