from twilio.rest import Client

from taskmaster.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


def get_twilio_client():
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
