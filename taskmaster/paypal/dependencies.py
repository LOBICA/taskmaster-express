from typing import Annotated

from fastapi import Depends

from . import client


def inject_paypal_client():
    return client.PayPalClient.get_client()


PayPalClient = Annotated[client.PayPalClient, Depends(inject_paypal_client)]
