"""
Project reporting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from betty.load import load
from betty.user import Verbosity

if TYPE_CHECKING:
    from betty.project import Project


async def report(project: Project) -> None:
    """
    Output a 'project report'.
    """
    original_verbosity = project.upstream.user.verbosity
    await project.upstream.user.set_verbosity(Verbosity.VERBOSE)
    try:
        await load(project)
    except BaseException:
        await project.upstream.user.set_verbosity(original_verbosity)
        raise
