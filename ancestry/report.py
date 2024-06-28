import logging

from betty.load import load
from betty.project import Project


async def report(project: Project) -> None:
    logging.getLogger("betty").setLevel(logging.DEBUG)
    await load(project)
