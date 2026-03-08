from fastapi import HTTPException, status

from api.application.dto.metrics import PassRatePoint, ProjectMetrics
from api.ports.outbound.project_repository import ProjectRepository
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository


async def get_project_metrics(
    project_id: str,
    projects: ProjectRepository,
    suites: TestSuiteRepository,
    runs: TestRunRepository,
) -> ProjectMetrics:
    project = await projects.find_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    project_suites = await suites.find_by_project(project_id, limit=1000)
    total_runs = 0
    all_trend: list[PassRatePoint] = []

    for suite in project_suites:
        suite_runs = await runs.find_by_suite(suite.id, limit=1000)
        total_runs += len(suite_runs)
        trend = await runs.find_pass_rate_trend(suite.id)
        all_trend.extend([PassRatePoint(date=p.date, pass_rate=p.pass_rate, total=p.total) for p in trend])

    overall = sum(p.pass_rate for p in all_trend) / len(all_trend) if all_trend else 0.0

    return ProjectMetrics(
        project_id=project_id,
        total_suites=len(project_suites),
        total_runs=total_runs,
        overall_pass_rate=overall,
        pass_rate_trend=all_trend[-30:],
    )
