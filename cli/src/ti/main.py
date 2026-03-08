import click

from ti.commands.auth import auth
from ti.commands.projects import projects
from ti.commands.push import push
from ti.commands.runs import runs
from ti.commands.suites import suites
from ti.commands.teams import teams


@click.group()
@click.version_option("0.1.0")
def cli() -> None:
    """Test Insights CLI — push and query test results."""


cli.add_command(auth)
cli.add_command(teams)
cli.add_command(projects)
cli.add_command(suites)
cli.add_command(runs)
cli.add_command(push)

if __name__ == "__main__":
    cli()
