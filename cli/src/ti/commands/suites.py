import click
from rich.console import Console
from rich.table import Table

from ti.client import http_client

console = Console()


@click.group()
def suites() -> None:
    """Manage test suites."""


@suites.command("list")
@click.argument("project_id")
def list_suites(project_id: str) -> None:
    resp = http_client.get(f"/api/v1/projects/{project_id}/suites")
    if resp.status_code != 200:
        console.print(f"[red]{resp.text}[/red]")
        return
    data = resp.json()
    table = Table("ID", "Name", "Description")
    for s in data:
        table.add_row(s["id"], s["name"], s.get("description") or "")
    console.print(table)


@suites.command("create")
@click.argument("project_id")
@click.option("--name", required=True)
@click.option("--description", default=None)
def create_suite(project_id: str, name: str, description: str | None) -> None:
    resp = http_client.post(f"/api/v1/projects/{project_id}/suites", json={"name": name, "description": description})
    if resp.status_code == 201:
        data = resp.json()
        console.print(f"[green]Created suite {data['id']}[/green]")
    else:
        console.print(f"[red]{resp.text}[/red]")


@suites.command("get")
@click.argument("suite_id")
def get_suite(suite_id: str) -> None:
    resp = http_client.get(f"/api/v1/suites/{suite_id}")
    if resp.status_code == 200:
        console.print_json(resp.text)
    else:
        console.print(f"[red]{resp.text}[/red]")


@suites.command("delete")
@click.argument("suite_id")
def delete_suite(suite_id: str) -> None:
    resp = http_client.delete(f"/api/v1/suites/{suite_id}")
    if resp.status_code == 204:
        console.print("[green]Deleted.[/green]")
    else:
        console.print(f"[red]{resp.text}[/red]")
