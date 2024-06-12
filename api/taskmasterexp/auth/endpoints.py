from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from taskmasterexp.database.dependencies import DBSession
from taskmasterexp.database.models import UserModel
from taskmasterexp.schemas.users import User

from .dependencies import CurrentUser, oauth2_scheme
from .helper import get_username_from_token
from .token import Token, TokenData, create_access_token, create_refresh_token

router = APIRouter(tags=["authentication"])


@router.post("/token", response_model=Token)
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

    token_data = TokenData.create_with_username(user.uuid)
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=Token)
async def refresh_authentication_token(
    refresh_token: Annotated[str, Depends(oauth2_scheme)],
    session: DBSession,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = get_username_from_token(refresh_token)

    stmt = select(UserModel).where(UserModel.uuid == UUID(username))
    results = await session.execute(stmt)
    user = results.scalar_one_or_none()

    if not user:
        raise credentials_exception

    token_data = TokenData.create_with_username(user.uuid)
    access_token = create_access_token(token_data, fresh=False)
    refresh_token = create_refresh_token(token_data)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.get("/users/me", response_model=User)
async def get_current_user(current_user: CurrentUser):
    return current_user
