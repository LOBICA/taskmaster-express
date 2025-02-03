from datetime import datetime, timedelta, timezone

import jwt
from pydantic import BaseModel, Field

from taskmaster.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)


class Token(BaseModel):
    sub: str
    scopes: list[str] = []

    @classmethod
    def create_with_username(cls, username):
        return cls(sub=f"username:{username}")

    @classmethod
    def decode_token(cls, token):
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        scope: str = data.get("scope", "")
        scopes = scope.split()
        return cls(scopes=scopes, **data)

    @property
    def username(self):
        type, username = self.sub.split(":")
        if type == "username":
            return username

        return None


class AccessTokenInput(BaseModel):
    access_token: str = Field(alias="accessToken")


class RefreshTokenInput(BaseModel):
    refresh_token: str = Field(alias="refreshToken")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str


def create_access_token(
    data: Token, fresh=True, expires_delta: timedelta | None = None
):
    to_encode = data.model_dump(exclude={"scopes"})
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


def create_refresh_token(data: Token, expires_delta: timedelta | None = None):
    to_encode = data.model_dump(exclude={"scopes"})
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
