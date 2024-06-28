import asyncio
from uuid import UUID

import click

from taskmasterexp.database.managers import UserManager
from taskmasterexp.schemas.users import User


@click.group()
def cli():
    pass


async def _create_user(name, email, password):
    async with UserManager.start_session() as manager:
        user = User(name=name, email=email)
        user = await manager.save(user, password=password)


@click.command()
@click.option("--name", prompt="Name")
@click.option("--email", prompt="Email")
def add_user(name, email):
    password = click.prompt("Password", hide_input=True)
    asyncio.run(_create_user(name, email, password))
    click.echo(f"User {name} added")


cli.add_command(add_user)


async def _change_password(user_id, password):
    async with UserManager.start_session() as manager:
        user = await manager.get(UUID(user_id))
        await manager.save(user, password=password)


@click.command()
@click.option("--user-id", prompt="User ID")
def change_user_password(user_id):
    password = click.prompt("Password", hide_input=True)
    asyncio.run(_change_password(user_id, password))
    click.echo(f"Password for user {user_id} changed")


cli.add_command(change_user_password)


if __name__ == "__main__":
    cli()
