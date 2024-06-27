from fastapi import APIRouter, status
from sqlalchemy import select

from taskmasterexp.auth.dependencies import CurrentUser
from taskmasterexp.database.dependencies import DBSession
from taskmasterexp.database.models import UserModel
from taskmasterexp.schemas.users import User, UserRegisterInput

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/me", response_model=User)
async def get_current_user(current_user: CurrentUser):
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(session: DBSession, current_user: CurrentUser):
    stmt = select(UserModel).where(UserModel.uuid == current_user.uuid)
    result = await session.execute(stmt)
    user = result.scalar_one()

    await session.delete(user)
    await session.commit()


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(session: DBSession, user: UserRegisterInput):
    new_user = UserModel(**user.dict(exclude={"password"}))
    session.add(new_user)
    new_user.set_password(user.password)
    await session.commit()

    return User.from_orm(new_user)
