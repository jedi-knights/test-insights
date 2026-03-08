from typing import Annotated

from fastapi import APIRouter, Depends

from api.adapters.inbound.http.dependencies import (
    get_case_repo,
    get_current_user,
    get_run_repo,
    get_suite_repo,
)
from api.application.dto.test_case import BulkCaseCreate, TestCaseResponse
from api.application.dto.test_run import TestRunCreate, TestRunResponse
from api.application.use_cases.runs import bulk_create_cases, create_run, get_run, list_runs
from api.domain.entities.user import User
from api.ports.outbound.test_case_repository import TestCaseRepository
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository

router = APIRouter(tags=["runs"])
Auth = Annotated[User, Depends(get_current_user)]


@router.get("/suites/{suite_id}/runs", response_model=list[TestRunResponse])
async def list_(
    _: Auth,
    suite_id: str,
    repo: Annotated[TestRunRepository, Depends(get_run_repo)],
    skip: int = 0,
    limit: int = 100,
) -> list[TestRunResponse]:
    return await list_runs.list_runs(suite_id, repo, skip=skip, limit=limit)


@router.post("/suites/{suite_id}/runs", response_model=TestRunResponse, status_code=201)
async def create(
    _: Auth,
    suite_id: str,
    request: TestRunCreate,
    suites: Annotated[TestSuiteRepository, Depends(get_suite_repo)],
    runs: Annotated[TestRunRepository, Depends(get_run_repo)],
) -> TestRunResponse:
    return await create_run.create_run(suite_id, request, suites, runs)


@router.get("/runs/{run_id}")
async def get(
    _: Auth,
    run_id: str,
    runs: Annotated[TestRunRepository, Depends(get_run_repo)],
    cases: Annotated[TestCaseRepository, Depends(get_case_repo)],
) -> get_run.RunDetail:
    return await get_run.get_run(run_id, runs, cases)


@router.post("/runs/{run_id}/cases", response_model=list[TestCaseResponse], status_code=201)
async def bulk_cases(
    _: Auth,
    run_id: str,
    request: BulkCaseCreate,
    runs: Annotated[TestRunRepository, Depends(get_run_repo)],
    cases: Annotated[TestCaseRepository, Depends(get_case_repo)],
) -> list[TestCaseResponse]:
    return await bulk_create_cases.bulk_create_cases(run_id, request, runs, cases)
