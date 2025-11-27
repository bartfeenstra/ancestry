from betty.project import Project
from betty.project.load import load
from betty.user import Verbosity


async def report(project: Project) -> None:
    original_verbosity = project.app.user.verbosity
    await project.app.user.set_verbosity(Verbosity.VERBOSE)
    try:
        await load(project)
    except BaseException:
        await project.app.user.set_verbosity(original_verbosity)
        raise
