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

from .token import decode_token, get_username_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    session: DBSession, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = get_username_from_token(decode_token(token))
        if not username:
            raise credentials_exception
    except (InvalidTokenError, ValueError):
        raise credentials_exception

    try:
        stmt = select(UserModel).where(UserModel.uuid == UUID(username))
        result = await session.execute(stmt)
        user = result.scalar_one()
    except (MultipleResultsFound, NoResultFound):
        raise credentials_exception

    return User.from_orm(user)


CurrentUser = Annotated[User, Depends(get_current_user)]
