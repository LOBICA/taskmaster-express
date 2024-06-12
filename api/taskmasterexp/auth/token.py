from datetime import datetime, timedelta, timezone

import jwt
from pydantic import BaseModel, Field

from taskmasterexp.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)


class TokenData(BaseModel):
    sub: str
    scopes: list[str] = []

    @classmethod
    def create_with_username(cls, username):
        return cls(sub=f"username:{username}")


class RefreshTokenInput(BaseModel):
    refresh_token: str = Field(alias="refreshToken")


class Token(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str


def create_access_token(
    data: TokenData, fresh=True, expires_delta: timedelta | None = None
):
    to_encode = data.dict(exclude={"scopes"})
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    scope = " ".join(data.scopes)
    to_encode.update({"exp": expire, "fresh": fresh, "scope": scope})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: TokenData, expires_delta: timedelta | None = None):
    to_encode = data.dict(exclude={"scopes"})
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES,
        )
    scopes = data.scopes.copy()
    scopes.append("refresh-token")
    scope = " ".join(scopes)
    to_encode.update({"exp": expire, "scope": scope})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_username_from_token(decoded_token: dict) -> str:
    subject: str = decoded_token.get("sub")
    type, username = subject.split(":")
    if type == "username":
        return username

    return None


def get_scopes_from_token(decoded_token: dict) -> list:
    scope: str = decoded_token.get("scope", "")
    return scope.split()
