from __future__ import annotations

from pathlib import Path
from typing import override

from betty.test_utils.locale import ProjectPotFileTestBase


class TestPotFile(ProjectPotFileTestBase):
    @override
    def command(self) -> str:
        return "betty update-translations ./ancestry ./ancestry/tests"

    @override
    def source_directory_path(self) -> Path:
        return self.project_directory_path() / "ancestry"

    @override
    def exclude_source_directory_paths(self) -> set[Path]:
        return {self.source_directory_path() / "tests"}

    @override
    def project_directory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent
