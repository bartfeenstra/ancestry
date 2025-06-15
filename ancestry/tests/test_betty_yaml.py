from pathlib import Path

from betty.config.file import assert_configuration_file
from betty.project.config import ProjectConfiguration


class TestBettyYaml:
    async def test(self) -> None:
        configuration_file_path = Path(__file__).parent.parent.parent / "betty.yaml"
        configuration = await ProjectConfiguration.new(configuration_file_path)
        assertion = await assert_configuration_file(configuration)
        assertion(configuration_file_path)
