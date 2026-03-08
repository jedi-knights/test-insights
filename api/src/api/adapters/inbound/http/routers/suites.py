from typing import Annotated

from fastapi import APIRouter, Depends

from api.adapters.inbound.http.dependencies import (
    get_current_user,
    get_project_repo,
    get_run_repo,
    get_suite_repo,
)
from api.application.dto.metrics import SuiteMetrics
from api.application.dto.test_suite import TestSuiteCreate, TestSuiteResponse, TestSuiteUpdate
from api.application.use_cases.suites import (
    create_suite,
    delete_suite,
    get_suite,
    list_suites,
    metrics as suite_metrics,
    update_suite,
)
from api.domain.entities.user import User
from api.ports.outbound.project_repository import ProjectRepository
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository

router = APIRouter(tags=["suites"])
Auth = Annotated[User, Depends(get_current_user)]


@router.get("/projects/{project_id}/suites", response_model=list[TestSuiteResponse])
async def list_(
    _: Auth,
    project_id: str,
    repo: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
    skip: int = 0,
    limit: int = 100,
) -> list[TestSuiteResponse]:
    return await list_suites.list_suites(project_id, repo, skip=skip, limit=limit)


@router.post("/projects/{project_id}/suites", response_model=TestSuiteResponse, status_code=201)
async def create(
    _: Auth,
    project_id: str,
    request: TestSuiteCreate,
    projects: Annotated[ProjectRepository, Depends(get_project_repo)],
    suites: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
) -> TestSuiteResponse:
    return await create_suite.create_suite(project_id, request, projects, suites)


@router.get("/suites/{suite_id}", response_model=TestSuiteResponse)
async def get(
    _: Auth,
    suite_id: str,
    repo: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
) -> TestSuiteResponse:
    return await get_suite.get_suite(suite_id, repo)


@router.put("/suites/{suite_id}", response_model=TestSuiteResponse)
async def update(
    _: Auth,
    suite_id: str,
    request: TestSuiteUpdate,
    repo: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
) -> TestSuiteResponse:
    return await update_suite.update_suite(suite_id, request, repo)


@router.delete("/suites/{suite_id}", status_code=204)
async def delete(
    _: Auth,
    suite_id: str,
    repo: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
) -> None:
    await delete_suite.delete_suite(suite_id, repo)


@router.get("/suites/{suite_id}/metrics", response_model=SuiteMetrics)
async def get_metrics(
    _: Auth,
    suite_id: str,
    suites: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
    runs: Annotated[TestRunRepository, Depends(get_run_repo)],
) -> SuiteMetrics:
    return await suite_metrics.get_suite_metrics(suite_id, suites, runs)
