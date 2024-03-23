import logging

from betty.app import App
from betty.load import load


async def report(app: App) -> None:
    logging.getLogger('betty').setLevel(logging.DEBUG)
    await load(app)
