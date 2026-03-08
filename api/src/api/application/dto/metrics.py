from pydantic import BaseModel


class PassRatePoint(BaseModel):
    date: str
    pass_rate: float
    total: int


class TeamMetrics(BaseModel):
    team_id: str
    total_projects: int
    total_suites: int
    total_runs: int
    overall_pass_rate: float
    pass_rate_trend: list[PassRatePoint]


class ProjectMetrics(BaseModel):
    project_id: str
    total_suites: int
    total_runs: int
    overall_pass_rate: float
    pass_rate_trend: list[PassRatePoint]


class SuiteMetrics(BaseModel):
    suite_id: str
    total_runs: int
    overall_pass_rate: float
    pass_rate_trend: list[PassRatePoint]
