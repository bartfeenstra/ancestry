"""
The report command.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, final, override

from betty.app import App
from betty.console import CommandDefinition
from betty.console.command import Command
from betty.console.project import add_project_argument
from betty.factory import Manufacturable

from ancestry.report import report

if TYPE_CHECKING:
    import argparse

    from betty.console import CommandFunction
    from betty.project import Project


@final
@CommandDefinition("report", label="Generate an ancestry report.")
class Report(Command, Manufacturable):
    """
    Output a 'project report'.
    """

    def __init__(self, app: App):
        self._app = app

    @override
    @App.require
    @classmethod
    async def new(cls, app: App, /) -> Self:
        return cls(app)

    @override
    async def configure(self, parser: argparse.ArgumentParser) -> CommandFunction:
        return await add_project_argument(parser, self._command_function, self._app)

    async def _command_function(self, project: Project) -> None:
        async with project:
            await report(project)
