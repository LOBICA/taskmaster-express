import click

from taskmasterexp.paypal.client import PayPalClient


@click.command()
def list_paypal_products():
    client = PayPalClient.get_client()
    products = client.list_products()
    for product in products:
        click.echo(f"{product.id_}: {product.name}")


@click.command()
@click.option("--name", prompt="Product name", help="The name of the product")
@click.option(
    "--description", prompt="Product description", help="The description of the product"
)
def add_paypal_product(name, description):
    client = PayPalClient.get_client()
    product_id = client.create_product(name, description)
    click.echo(f"Product added {product_id}")


@click.command()
@click.option("--product-id", prompt="Product ID", help="The ID of the product")
def list_subscription_plans(product_id):
    client = PayPalClient.get_client()
    subscription_plans = client.list_subscription_plans(product_id)
    for plan in subscription_plans:
        click.echo(f"{plan.id_}: {plan.name}")


@click.command()
@click.option("--product-id", prompt="Product ID", help="The ID of the product")
@click.option("--name", prompt="Plan name", help="The name of the plan")
@click.option(
    "--description", prompt="Plan description", help="The description of the plan"
)
@click.option(
    "--monthly-price", prompt="Monthly price", help="The monthly price of the plan"
)
@click.option(
    "--trial-months",
    prompt="Trial months",
    help="The number of months for the trial period",
)
def add_subscription_plan(
    product_id,
    name,
    description,
    monthly_price,
    trial_months,
):
    client = PayPalClient.get_client()
    plan_id = client.create_subscription_plan(
        product_id=product_id,
        name=name,
        description=description,
        monthly_price=monthly_price,
        trial_months=int(trial_months),
    )
    click.echo(f"Plan added {plan_id}")
