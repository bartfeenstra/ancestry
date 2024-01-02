import logging
from pathlib import Path

from betty.app import App
from betty.asyncio import sync
from betty.load import load
from betty.logging import CliHandler


@sync
async def report() -> None:
    async with App() as app:
        await app.project.configuration.read(Path(__file__).parent.parent / 'betty.yaml')
        logging.getLogger().addHandler(CliHandler())
        logging.getLogger('betty').setLevel(logging.DEBUG)
        await load(app)
