from __future__ import annotations  # noqa D100

from typing import TYPE_CHECKING, final, Self

from betty.app.factory import AppDependentFactory
from betty.cli.commands import command, Command, project_option
from betty.locale.localizable import _
from betty.plugin import ShorthandPluginBase
from typing_extensions import override

from ancestry.report import report

if TYPE_CHECKING:
    from betty.project import Project
    import asyncclick as click
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
    async def click_command(self) -> click.Command:
        localizer = await self._app.localizer
        description = self.plugin_description()

        @command(
            self.plugin_id(),
            short_help=self.plugin_label().localize(localizer),
            help=description.localize(localizer)
            if description
            else self.plugin_label().localize(localizer),
        )
        @project_option
        async def _report(project: Project) -> None:
            await report(project)

        return _report
