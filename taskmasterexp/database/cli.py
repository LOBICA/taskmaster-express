import asyncio

import click
from sqlalchemy.exc import IntegrityError

from .redis import cleanup_redis as cleanup_redis_process
from .seed import seed as seed_process


@click.command()
def seed():
    click.echo("Seeding database...")
    try:
        asyncio.run(seed_process())
    except IntegrityError:
        click.echo("Could not seed database. Database may be already seeded.")
    click.echo("Done!")


@click.command()
def cleanup_redis():
    click.echo("Cleaning up Redis...")
    asyncio.run(cleanup_redis_process())
    click.echo("Done!")
