import cProfile
import logging
from pathlib import Path
import pstats

from betty.app import App
from betty.asyncio import sync
from betty.generate import generate
from betty.load import load


PROFILE_FILE_PATH = Path('profile.stats')

@sync
async def do_the_thing() -> None:
    async with App() as app:
        await app.project.configuration.read(Path('betty.yaml'))
        await load(app)
        await generate(app)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    with cProfile.Profile() as profile:
        profile.runcall(do_the_thing)
        profile.dump_stats(PROFILE_FILE_PATH)

    stats = pstats.Stats(str(PROFILE_FILE_PATH))
    stats.sort_stats('tottime')
    stats.reverse_order()
    stats.print_stats()
