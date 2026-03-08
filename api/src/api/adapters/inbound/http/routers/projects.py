from typing import Annotated

from fastapi import APIRouter, Depends

from api.adapters.inbound.http.dependencies import (
    get_current_user,
    get_project_repo,
    get_run_repo,
    get_suite_repo,
    get_team_repo,
)
from api.application.dto.metrics import ProjectMetrics
from api.application.dto.project import ProjectCreate, ProjectResponse, ProjectUpdate
from api.application.use_cases.projects import (
    create_project,
    delete_project,
    get_project,
    list_projects,
    metrics as project_metrics,
    update_project,
)
from api.domain.entities.user import User
from api.ports.outbound.project_repository import ProjectRepository
from api.ports.outbound.team_repository import TeamRepository
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository

router = APIRouter(tags=["projects"])
Auth = Annotated[User, Depends(get_current_user)]


@router.get("/teams/{team_id}/projects", response_model=list[ProjectResponse])
async def list_(
    _: Auth,
    team_id: str,
    repo: Annotated[ProjectRepository, Depends(get_project_repo)],
    skip: int = 0,
    limit: int = 100,
) -> list[ProjectResponse]:
    return await list_projects.list_projects(team_id, repo, skip=skip, limit=limit)


@router.post("/teams/{team_id}/projects", response_model=ProjectResponse, status_code=201)
async def create(
    _: Auth,
    team_id: str,
    request: ProjectCreate,
    teams: Annotated[TeamRepository, Depends(get_team_repo)],
    projects: Annotated[ProjectRepository, Depends(get_project_repo)],
) -> ProjectResponse:
    return await create_project.create_project(team_id, request, teams, projects)


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get(
    _: Auth,
    project_id: str,
    repo: Annotated[ProjectRepository, Depends(get_project_repo)],
) -> ProjectResponse:
    return await get_project.get_project(project_id, repo)


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update(
    _: Auth,
    project_id: str,
    request: ProjectUpdate,
    repo: Annotated[ProjectRepository, Depends(get_project_repo)],
) -> ProjectResponse:
    return await update_project.update_project(project_id, request, repo)


@router.delete("/projects/{project_id}", status_code=204)
async def delete(
    _: Auth,
    project_id: str,
    repo: Annotated[ProjectRepository, Depends(get_project_repo)],
) -> None:
    await delete_project.delete_project(project_id, repo)


@router.get("/projects/{project_id}/metrics", response_model=ProjectMetrics)
async def get_metrics(
    _: Auth,
    project_id: str,
    projects: Annotated[ProjectRepository, Depends(get_project_repo)],
    suites: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
    runs: Annotated[TestRunRepository, Depends(get_run_repo)],
) -> ProjectMetrics:
    return await project_metrics.get_project_metrics(project_id, projects, suites, runs)
