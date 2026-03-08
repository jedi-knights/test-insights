from fastapi import HTTPException, status

from api.application.dto.metrics import PassRatePoint, SuiteMetrics
from api.ports.outbound.test_run_repository import TestRunRepository
from api.ports.outbound.test_suite_repository import TestSuiteRepository


async def get_suite_metrics(
    suite_id: str,
    suites: TestSuiteRepository,
    runs: TestRunRepository,
) -> SuiteMetrics:
    suite = await suites.find_by_id(suite_id)
    if not suite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suite not found")

    suite_runs = await runs.find_by_suite(suite_id, limit=1000)
    trend_points = await runs.find_pass_rate_trend(suite_id)
    trend = [PassRatePoint(date=p.date, pass_rate=p.pass_rate, total=p.total) for p in trend_points]
    overall = sum(p.pass_rate for p in trend) / len(trend) if trend else 0.0

    return SuiteMetrics(
        suite_id=suite_id,
        total_runs=len(suite_runs),
        overall_pass_rate=overall,
        pass_rate_trend=trend,
    )
