import click
import httpx
from rich.console import Console

from ti.client import http_client
from ti.config import store

console = Console()


@click.group()
def auth() -> None:
    """Authentication commands."""


@auth.command()
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
@click.option("--api-url", default=None, help="API base URL")
def login(email: str, password: str, api_url: str | None) -> None:
    """Log in and store tokens."""
    if api_url:
        store.set_key("api_url", api_url)
    try:
        resp = http_client.post("/api/v1/auth/login", json={"email": email, "password": password})
        if resp.status_code == 200:
            data = resp.json()
            store.set_key("access_token", data["access_token"])
            store.set_key("refresh_token", data["refresh_token"])
            console.print("[green]Logged in successfully.[/green]")
        else:
            console.print(f"[red]Login failed: {resp.json().get('detail', resp.text)}[/red]")
    except httpx.ConnectError:
        console.print("[red]Cannot connect to API. Is it running?[/red]")


@auth.command()
def logout() -> None:
    """Log out and clear stored tokens."""
    refresh_token = store.get("refresh_token")
    if refresh_token:
        try:
            http_client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
        except httpx.ConnectError:
            pass
    store.delete_key("access_token")
    store.delete_key("refresh_token")
    console.print("[green]Logged out.[/green]")


@auth.command()
def whoami() -> None:
    """Show current user info."""
    resp = http_client.get("/api/v1/auth/me")
    if resp.status_code == 200:
        data = resp.json()
        console.print(f"[cyan]{data['email']}[/cyan] (id: {data['id']})")
    elif resp.status_code == 401:
        console.print("[yellow]Not logged in.[/yellow]")
    else:
        console.print(f"[red]Error: {resp.text}[/red]")
