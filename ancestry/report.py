import logging

from betty.project import Project
from betty.project.load import load


async def report(project: Project) -> None:
    logging.getLogger("betty").setLevel(logging.DEBUG)
    await load(project)
