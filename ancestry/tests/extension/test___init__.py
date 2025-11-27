from typing import override

from betty.test_utils.project.extension import (
    ExtensionTestBase,
    ExtensionPluginTestBase,
)

from ancestry.extension import Ancestry
from betty.app import App
from betty.project import Project
from betty.project.extension import Extension
import pytest

from betty.plugin import PluginDefinition


class TestAncestryPlugin(ExtensionPluginTestBase):
    @override
    @pytest.fixture
    def sut(self) -> PluginDefinition:
        return Ancestry.plugin


class TestAncestry(ExtensionTestBase):
    @override
    @pytest.fixture
    async def sut(self, temporary_app: App) -> Extension:
        async with Project.new_temporary(temporary_app) as project, project:
            return Ancestry(project)
