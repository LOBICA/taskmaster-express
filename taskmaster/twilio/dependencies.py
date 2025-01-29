"""Twilio client for FastAPI dependency injection."""
from typing import Annotated

from fastapi import Depends

from . import client


# TwilioClient dependency
async def inject_twilio_client() -> client.Client:
    return client.get_twilio_client()


TwilioClient = Annotated[client.Client, Depends(inject_twilio_client)]
