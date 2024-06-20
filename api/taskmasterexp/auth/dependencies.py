from typing import Annotated
from uuid import UUID

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from taskmasterexp.database.dependencies import DBSession
from taskmasterexp.database.models import UserModel
from taskmasterexp.schemas.users import User

from .token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def _get_current_user(session: DBSession, encoded_token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = Token.decode_token(encoded_token)
        if not token.username:
            raise credentials_exception
    except (InvalidTokenError, ValueError):
        raise credentials_exception

    try:
        stmt = select(UserModel).where(UserModel.uuid == UUID(token.username))
        result = await session.execute(stmt)
        user = result.scalar_one()
    except (MultipleResultsFound, NoResultFound):
        raise credentials_exception

    return User.from_orm(user)


async def get_current_user(
    session: DBSession, encoded_token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    return await _get_current_user(session, encoded_token)


async def get_current_user_ws(session: DBSession, token: str) -> User:
    return await _get_current_user(session, token)


CurrentUser = Annotated[User, Depends(get_current_user)]

CurrentUserWS = Annotated[User, Depends(get_current_user_ws)]
