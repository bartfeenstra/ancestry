from typing import override

from betty.test_utils.project.extension import (
    ExtensionTestBase,
    ExtensionDefinitionTestBase,
)

from ancestry.extension import Ancestry
from betty.app import App
from betty.project import Project
from betty.project.extension import Extension
import pytest

from betty.plugin import PluginDefinition


class TestAncestryDefinition(ExtensionDefinitionTestBase):
    @override
    @pytest.fixture
    def sut(self) -> PluginDefinition:
        return Ancestry.plugin


class TestAncestry(ExtensionTestBase):
    @override
    @pytest.fixture
    async def sut(self, temporary_app: App) -> Extension:
        async with Project.new_temporary(temporary_app) as project, project:
            return await Ancestry.new_for_project(project)
