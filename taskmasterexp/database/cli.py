import asyncio

import click
from sqlalchemy.exc import IntegrityError

from .seed import seed as seed_process


@click.command()
def seed():
    click.echo("Seeding database...")
    try:
        asyncio.run(seed_process())
    except IntegrityError:
        click.echo("Could not seed database. Database may be already seeded.")
    click.echo("Done!")
