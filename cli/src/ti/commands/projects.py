import click
from rich.console import Console
from rich.table import Table

from ti.client import http_client

console = Console()


@click.group()
def projects() -> None:
    """Manage projects."""


@projects.command("list")
@click.argument("team_id")
def list_projects(team_id: str) -> None:
    resp = http_client.get(f"/api/v1/teams/{team_id}/projects")
    if resp.status_code != 200:
        console.print(f"[red]{resp.text}[/red]")
        return
    data = resp.json()
    table = Table("ID", "Name", "Description")
    for p in data:
        table.add_row(p["id"], p["name"], p.get("description") or "")
    console.print(table)


@projects.command("create")
@click.argument("team_id")
@click.option("--name", required=True)
@click.option("--description", default=None)
def create_project(team_id: str, name: str, description: str | None) -> None:
    resp = http_client.post(f"/api/v1/teams/{team_id}/projects", json={"name": name, "description": description})
    if resp.status_code == 201:
        data = resp.json()
        console.print(f"[green]Created project {data['id']}[/green]")
    else:
        console.print(f"[red]{resp.text}[/red]")


@projects.command("get")
@click.argument("project_id")
def get_project(project_id: str) -> None:
    resp = http_client.get(f"/api/v1/projects/{project_id}")
    if resp.status_code == 200:
        console.print_json(resp.text)
    else:
        console.print(f"[red]{resp.text}[/red]")


@projects.command("delete")
@click.argument("project_id")
def delete_project(project_id: str) -> None:
    resp = http_client.delete(f"/api/v1/projects/{project_id}")
    if resp.status_code == 204:
        console.print("[green]Deleted.[/green]")
    else:
        console.print(f"[red]{resp.text}[/red]")
