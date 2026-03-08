from fastapi import HTTPException, status

from api.application.dto.metrics import PassRatePoint, TeamMetrics
from api.ports.outbound.project_repository import ProjectRepository
from api.ports.outbound.team_repository import TeamRepository
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository


async def get_team_metrics(
    team_id: str,
    teams: TeamRepository,
    projects: ProjectRepository,
    suites: TestSuiteRepository,
    runs: TestRunRepository,
) -> TeamMetrics:
    team = await teams.find_by_id(team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    team_projects = await projects.find_by_team(team_id, limit=1000)
    total_suites = 0
    total_runs = 0
    all_trend_points: list[PassRatePoint] = []

    for project in team_projects:
        project_suites = await suites.find_by_project(project.id, limit=1000)
        total_suites += len(project_suites)
        for suite in project_suites:
            suite_runs = await runs.find_by_suite(suite.id, limit=1000)
            total_runs += len(suite_runs)
            trend = await runs.find_pass_rate_trend(suite.id)
            all_trend_points.extend([PassRatePoint(date=p.date, pass_rate=p.pass_rate, total=p.total) for p in trend])

    overall_pass_rate = 0.0
    if all_trend_points:
        overall_pass_rate = sum(p.pass_rate for p in all_trend_points) / len(all_trend_points)

    return TeamMetrics(
        team_id=team_id,
        total_projects=len(team_projects),
        total_suites=total_suites,
        total_runs=total_runs,
        overall_pass_rate=overall_pass_rate,
        pass_rate_trend=all_trend_points[-30:],
    )
