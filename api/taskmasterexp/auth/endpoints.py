from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from taskmasterexp.database.dependencies import AsyncSession
from taskmasterexp.database.models import UserModel

from .token import Token, create_access_token

router = APIRouter(tags=["authentication"])


@router.post("/token")
async def get_authentication_token(
    session: AsyncSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
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

    access_token = create_access_token({"sub": f"username:{user.uuid}"})
    return Token(
        access_token=access_token,
        token_type="bearer",
    )
