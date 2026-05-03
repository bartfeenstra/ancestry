from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from betty.file import read
from betty.project import Project
from betty.project.data import ProjectConfiguration

if TYPE_CHECKING:
    from betty.app import App


class TestBettyYaml:
    async def test(self, isolated_app: App) -> None:
        project_directory = Path(__file__).parent.parent.parent
        data = ProjectConfiguration.data().porter.load(
            yaml.safe_load(await read(project_directory / "betty.yaml"))
        )
        async with await Project.new(
            isolated_app, data, directory=project_directory
        ) as _:
            pass
