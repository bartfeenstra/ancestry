from pathlib import Path

# Import betty.app first to prevent a circular import error.
import betty.app  # noqa F401
from betty.project import ProjectConfiguration


class TestBettyYaml:
    async def test(self) -> None:
        configuration_file_path = Path(__file__).parent.parent.parent / "betty.yaml"
        configuration = ProjectConfiguration()
        await configuration.read(configuration_file_path)
