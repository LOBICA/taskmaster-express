from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select

from taskmaster.database.dependencies import DBSession
from taskmaster.database.models import UserModel
from taskmaster.settings import FB_LOGIN_REDIRECT

from .fb import get_authorization_url, get_fb_info, get_fb_info_from_token
from .token import (
    AccessTokenInput,
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

    if user.disabled:
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

    if user.disabled:
        raise credentials_exception

    token_data = Token.create_with_username(user.uuid)
    access_token = create_access_token(token_data, fresh=False)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.get("/auth/fb")
async def facebook_login():
    authorization_url = await get_authorization_url()
    return RedirectResponse(url=authorization_url)


@router.get("/auth/fb-callback")
async def fb_callback(session: DBSession, request: Request):
    fb_info = await get_fb_info(str(request.url))
    stmt = select(UserModel).where(UserModel.fb_user_id == fb_info.fb_user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        stmt = select(UserModel).where(UserModel.email == fb_info.email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            user = UserModel(
                name=fb_info.name,
                email=fb_info.email,
            )
            session.add(user)

        user.fb_user_id = fb_info.fb_user_id

    user.fb_access_token = fb_info.token
    await session.commit()

    redirect_url = f"{FB_LOGIN_REDIRECT}?fb_token={user.fb_access_token}"
    return RedirectResponse(url=redirect_url)


@router.post("/fb_login")
async def facebok_login(session: DBSession, token: AccessTokenInput):
    fb_info = await get_fb_info_from_token(token.access_token)

    stmt = select(UserModel).where(UserModel.fb_user_id == fb_info.fb_user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        stmt = select(UserModel).where(UserModel.email == fb_info.email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            user = UserModel(
                name=fb_info.name,
                email=fb_info.email,
            )
            session.add(user)

        user.fb_user_id = fb_info.fb_user_id

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is disabled",
        )

    user.fb_access_token = fb_info.token
    await session.commit()

    token_data = Token.create_with_username(user.uuid)
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
