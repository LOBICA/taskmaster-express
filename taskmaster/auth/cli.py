import asyncio
from datetime import timedelta
from uuid import UUID

import click

from taskmaster.auth.token import Token, create_app_token
from taskmaster.database.managers import UserManager
from taskmaster.schemas.users import User


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


@click.command()
@click.option("--app-name", prompt="App name")
def generate_app_token(app_name):
    token = Token.create_with_username(app_name)
    app_token = create_app_token(token)
    click.echo(f"App token for {app_name}: {app_token}")
