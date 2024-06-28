import click
from betty.cli.commands import pass_project, command
from betty.project import Project

from ancestry.report import report


@click.command("report", help="Generate an ancestry report.")
@pass_project
@command
async def _report(project: Project) -> None:
    await report(project)
