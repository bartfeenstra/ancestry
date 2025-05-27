from betty.project import Project
from betty.project.load import load
from betty.user import Verbosity


async def report(project: Project) -> None:
    original_verbosity = project.app.user.verbosity
    project.app.user.verbosity = Verbosity.VERBOSE
    try:
        await load(project)
    except BaseException:
        project.app.user.verbosity = original_verbosity
        raise
