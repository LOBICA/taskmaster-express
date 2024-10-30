import asyncio

import click

from .seed import seed as seed_process


@click.command()
def seed():
    click.echo("Seeding database...")
    asyncio.run(seed_process())
    click.echo("Done!")
