from betty.cli.commands import pass_project, command
from betty.project import Project

from ancestry.report import report


@command("report", help="Generate an ancestry report.")
@pass_project
async def _report(project: Project) -> None:
    await report(project)
