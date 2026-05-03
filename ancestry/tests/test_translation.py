from __future__ import annotations

from pathlib import Path
from typing import override

from betty.locale.translation import update_translations
from betty.test_utils.locale import PotFileTestBase
from betty.user.no_op import NoOpUser


class TestPotFile(PotFileTestBase):
    @override
    def command(self) -> str:
        return "betty update-translations ancestry ./ancestry"

    @override
    def asset_directory(self) -> Path:
        return Path(__file__).parent.parent.parent / "assets"

    @override
    async def update_translations(
        self, output_assets_directory_path_override: Path
    ) -> None:
        await update_translations(
            output_assets_directory_path_override,
            [Path(__file__).parent.parent],
            excludes=(),
            user=NoOpUser(),
        )
