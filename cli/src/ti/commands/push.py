"""Push test results to Test Insights."""

import os
import sys
from datetime import datetime, timezone

import click
from rich.console import Console
from rich.table import Table

from ti.client import http_client
from ti.parsers import go_json, junit, pytest_json, tap
from ti.parsers.base import ParsedRun

console = Console()

FORMAT_PARSERS = {
    "junit": junit.parse,
    "pytest-json": pytest_json.parse,
    "go-json": go_json.parse,
    "tap": tap.parse,
}

BUILD_SYSTEM_ENV = {
    "GITHUB_ACTIONS": "github_actions",
    "GITLAB_CI": "gitlab_ci",
    "JENKINS_URL": "jenkins",
    "CIRCLECI": "circleci",
}

GITHUB_METADATA_KEYS = [
    "GITHUB_REPOSITORY", "GITHUB_REF", "GITHUB_SHA", "GITHUB_RUN_ID",
    "GITHUB_WORKFLOW", "GITHUB_ACTOR",
]
GITLAB_METADATA_KEYS = [
    "CI_PROJECT_PATH", "CI_COMMIT_REF_NAME", "CI_COMMIT_SHA",
    "CI_PIPELINE_ID", "CI_JOB_ID",
]
JENKINS_METADATA_KEYS = ["JENKINS_URL", "JOB_NAME", "BUILD_NUMBER", "GIT_BRANCH", "GIT_COMMIT"]
CIRCLECI_METADATA_KEYS = ["CIRCLE_PROJECT_REPONAME", "CIRCLE_BRANCH", "CIRCLE_SHA1", "CIRCLE_BUILD_NUM"]


def detect_build_system() -> tuple[str, dict]:
    for env_var, name in BUILD_SYSTEM_ENV.items():
        if os.environ.get(env_var):
            metadata = {}
            if name == "github_actions":
                metadata = {k: os.environ.get(k) for k in GITHUB_METADATA_KEYS if os.environ.get(k)}
                return name, metadata
            elif name == "gitlab_ci":
                metadata = {k: os.environ.get(k) for k in GITLAB_METADATA_KEYS if os.environ.get(k)}
                return name, metadata
            elif name == "jenkins":
                metadata = {k: os.environ.get(k) for k in JENKINS_METADATA_KEYS if os.environ.get(k)}
                return name, metadata
            elif name == "circleci":
                metadata = {k: os.environ.get(k) for k in CIRCLECI_METADATA_KEYS if os.environ.get(k)}
                return name, metadata
    return "local", {}


def get_branch_from_env() -> str | None:
    for key in ["GITHUB_REF_NAME", "CI_COMMIT_REF_NAME", "GIT_BRANCH", "CIRCLE_BRANCH"]:
        v = os.environ.get(key)
        if v:
            return v
    return None


def get_commit_from_env() -> str | None:
    for key in ["GITHUB_SHA", "CI_COMMIT_SHA", "GIT_COMMIT", "CIRCLE_SHA1"]:
        v = os.environ.get(key)
        if v:
            return v
    return None


@click.command()
@click.argument("suite_id")
@click.option("--file", "-f", "filepath", default=None, help="Path to test result file (stdin if omitted)")
@click.option("--format", "fmt", required=True, type=click.Choice(list(FORMAT_PARSERS.keys())), help="Report format")
@click.option("--branch", default=None, help="Branch name (auto-detected from CI env)")
@click.option("--commit", default=None, help="Commit SHA (auto-detected from CI env)")
def push(suite_id: str, filepath: str | None, fmt: str, branch: str | None, commit: str | None) -> None:
    """Parse and push test results to a suite."""
    if filepath:
        with open(filepath) as fh:
            content = fh.read()
    else:
        content = sys.stdin.read()

    parser = FORMAT_PARSERS[fmt]
    try:
        run: ParsedRun = parser(content)
    except Exception as e:
        console.print(f"[red]Failed to parse {fmt}: {e}[/red]")
        raise SystemExit(1)

    build_system, metadata = detect_build_system()
    branch = branch or get_branch_from_env()
    commit = commit or get_commit_from_env()

    run_payload = {
        "build_system": build_system,
        "branch": branch,
        "commit_sha": commit,
        "status": "passed" if run.failed_tests == 0 and run.error_tests == 0 else "failed",
        "total_tests": run.total_tests,
        "passed_tests": run.passed_tests,
        "failed_tests": run.failed_tests,
        "skipped_tests": run.skipped_tests,
        "error_tests": run.error_tests,
        "duration_seconds": run.duration_seconds,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata,
    }

    resp = http_client.post(f"/api/v1/suites/{suite_id}/runs", json=run_payload)
    if resp.status_code != 201:
        console.print(f"[red]Failed to create run: {resp.text}[/red]")
        raise SystemExit(1)

    run_id = resp.json()["id"]

    cases_payload = {
        "cases": [
            {
                "name": c.name,
                "classname": c.classname,
                "file_path": c.file_path,
                "status": c.status,
                "duration_seconds": c.duration_seconds,
                "error_message": c.error_message,
                "stack_trace": c.stack_trace,
            }
            for c in run.cases
        ]
    }
    if cases_payload["cases"]:
        resp = http_client.post(f"/api/v1/runs/{run_id}/cases", json=cases_payload)
        if resp.status_code != 201:
            console.print(f"[red]Failed to push cases: {resp.text}[/red]")
            raise SystemExit(1)

    # Print summary
    table = Table(title=f"Run {run_id}")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Status", "[green]passed[/green]" if run.failed_tests == 0 and run.error_tests == 0 else "[red]failed[/red]")
    table.add_row("Total", str(run.total_tests))
    table.add_row("Passed", f"[green]{run.passed_tests}[/green]")
    table.add_row("Failed", f"[red]{run.failed_tests}[/red]")
    table.add_row("Skipped", str(run.skipped_tests))
    table.add_row("Errors", str(run.error_tests))
    table.add_row("Build System", build_system)
    console.print(table)
