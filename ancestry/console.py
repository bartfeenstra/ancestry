from __future__ import annotations  # noqa D100

from typing import TYPE_CHECKING, final, Self

from betty.app.factory import AppDependentFactory
from betty.console.project import add_project_argument
from betty.console.command import Command, CommandFunction
from betty.locale.localizable import _
from betty.plugin import ShorthandPluginBase
from typing_extensions import override

from ancestry.report import report

if TYPE_CHECKING:
    import argparse
    from betty.project import Project
    from betty.app import App


@final
class Report(ShorthandPluginBase, AppDependentFactory, Command):
    _plugin_id = "report"
    _plugin_label = _("Generate an ancestry report.")

    def __init__(self, app: App):
        self._app = app

    @override
    @classmethod
    async def new_for_app(cls, app: App) -> Self:
        return cls(app)

    @override
    async def configure(self, parser: argparse.ArgumentParser) -> CommandFunction:
        return await add_project_argument(parser, self._command_function, self._app)

    async def _command_function(self, project: Project) -> None:
        async with project:
            await report(project)
