import asyncio

from taskmaster.settings import WHATSAPP_NUMBER

from .dependencies import TwilioClient
from .errors import MessageTooLongError


async def send_split_message(client: TwilioClient, text: str, destination: str):
    messages = []
    char_count = 0

    paragraphs = text.split("\n")

    if any(len(paragraph) > 1300 for paragraph in paragraphs):
        raise MessageTooLongError

    for paragraph in paragraphs:
        paragraph_len = len(paragraph)
        char_count += paragraph_len
        if char_count > 1300:
            send_message(client, "\n".join(messages), destination=destination)
            messages = []
            char_count = paragraph_len
            # Add a delay between messages
            await asyncio.sleep(1)
        messages.append(paragraph)
    send_message(client, "\n".join(messages), destination=destination)


def send_message(client: TwilioClient, text: str, destination: str):
    client.messages.create(
        from_=f"whatsapp:{WHATSAPP_NUMBER}", body=text, to=destination
    )
