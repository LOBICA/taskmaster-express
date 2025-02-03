import click

from taskmaster.auth import cli as auth_cli
from taskmaster.database import cli as database_cli
from taskmaster.paypal import cli as paypal_cli


@click.group()
def cli():
    "Administrator tasks for Taskmaster backend"


cli.add_command(database_cli.seed)
cli.add_command(database_cli.cleanup_redis)

cli.add_command(paypal_cli.list_paypal_products)
cli.add_command(paypal_cli.add_paypal_product)
cli.add_command(paypal_cli.list_subscription_plans)
cli.add_command(paypal_cli.add_subscription_plan)

cli.add_command(auth_cli.add_user)
cli.add_command(auth_cli.change_user_password)


if __name__ == "__main__":
    cli()
