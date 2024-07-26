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
