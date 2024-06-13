from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select

from taskmasterexp.database.dependencies import DBSession
from taskmasterexp.database.models import UserModel
from taskmasterexp.schemas.users import User

from .dependencies import CurrentUser
from .token import (
    RefreshTokenInput,
    Token,
    TokenResponse,
    create_access_token,
    create_refresh_token,
)

router = APIRouter(tags=["authentication"])


@router.post("/token", response_model=TokenResponse)
async def get_authentication_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: DBSession
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    stmt = select(UserModel).where(UserModel.email == form_data.username)
    results = await session.execute(stmt)
    user = results.scalar_one_or_none()

    if not user:
        raise credentials_exception

    if not user.verify_password(form_data.password):
        raise credentials_exception

    token_data = Token.create_with_username(user.uuid)
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_authentication_token(
    refresh_token_input: RefreshTokenInput,
    session: DBSession,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    refresh_token = refresh_token_input.refresh_token

    try:
        token = Token.decode_token(refresh_token)
    except InvalidTokenError:
        raise credentials_exception

    if "refresh-token" not in token.scopes:
        raise credentials_exception

    stmt = select(UserModel).where(UserModel.uuid == UUID(token.username))
    results = await session.execute(stmt)
    user = results.scalar_one_or_none()

    if not user:
        raise credentials_exception

    token_data = Token.create_with_username(user.uuid)
    access_token = create_access_token(token_data, fresh=False)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.get("/users/me", response_model=User)
async def get_current_user(current_user: CurrentUser):
    return current_user
