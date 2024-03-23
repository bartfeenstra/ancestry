import click

from betty.app import App
from betty.cli import app_command

from ancestry.report import report


@click.command(help='Generate an ancestry report.')
@app_command
async def _report(app: App) -> None:
    await report(app)
