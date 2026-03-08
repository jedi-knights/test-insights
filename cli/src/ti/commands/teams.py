import click
from rich.console import Console
from rich.table import Table

from ti.client import http_client

console = Console()


@click.group()
def teams() -> None:
    """Manage teams."""


@teams.command("list")
def list_teams() -> None:
    resp = http_client.get("/api/v1/teams")
    if resp.status_code != 200:
        console.print(f"[red]{resp.text}[/red]")
        return
    data = resp.json()
    table = Table("ID", "Name", "Description")
    for t in data:
        table.add_row(t["id"], t["name"], t.get("description") or "")
    console.print(table)


@teams.command("create")
@click.option("--name", required=True)
@click.option("--description", default=None)
def create_team(name: str, description: str | None) -> None:
    resp = http_client.post("/api/v1/teams", json={"name": name, "description": description})
    if resp.status_code == 201:
        data = resp.json()
        console.print(f"[green]Created team {data['id']}[/green]")
    else:
        console.print(f"[red]{resp.text}[/red]")


@teams.command("get")
@click.argument("team_id")
def get_team(team_id: str) -> None:
    resp = http_client.get(f"/api/v1/teams/{team_id}")
    if resp.status_code == 200:
        console.print_json(resp.text)
    else:
        console.print(f"[red]{resp.text}[/red]")


@teams.command("delete")
@click.argument("team_id")
def delete_team(team_id: str) -> None:
    resp = http_client.delete(f"/api/v1/teams/{team_id}")
    if resp.status_code == 204:
        console.print("[green]Deleted.[/green]")
    else:
        console.print(f"[red]{resp.text}[/red]")
