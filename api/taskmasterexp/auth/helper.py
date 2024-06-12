import jwt

from taskmasterexp.settings import ALGORITHM, SECRET_KEY


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_username_from_token(token: str) -> str:
    payload = decode_token(token)
    subject: str = payload.get("sub")
    type, username = subject.split(":")
    if type == "username":
        return username

    return None
