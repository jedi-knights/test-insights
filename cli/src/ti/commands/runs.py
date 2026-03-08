import click
from rich.console import Console
from rich.table import Table

from ti.client import http_client

console = Console()


@click.group()
def runs() -> None:
    """Manage test runs."""


@runs.command("list")
@click.argument("suite_id")
def list_runs(suite_id: str) -> None:
    resp = http_client.get(f"/api/v1/suites/{suite_id}/runs")
    if resp.status_code != 200:
        console.print(f"[red]{resp.text}[/red]")
        return
    data = resp.json()
    table = Table("ID", "Status", "Total", "Passed", "Failed", "Branch")
    for r in data:
        table.add_row(r["id"], r["status"], str(r["total_tests"]), str(r["passed_tests"]), str(r["failed_tests"]), r.get("branch") or "")
    console.print(table)


@runs.command("get")
@click.argument("run_id")
def get_run(run_id: str) -> None:
    resp = http_client.get(f"/api/v1/runs/{run_id}")
    if resp.status_code == 200:
        console.print_json(resp.text)
    else:
        console.print(f"[red]{resp.text}[/red]")
