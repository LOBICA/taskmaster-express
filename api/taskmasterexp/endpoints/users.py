from fastapi import APIRouter, status

from taskmasterexp.auth.dependencies import CurrentUser
from taskmasterexp.database.dependencies import UserManager
from taskmasterexp.schemas.users import User, UserRegisterInput, UserResponse

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: CurrentUser):
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(manager: UserManager, current_user: CurrentUser):
    await manager.delete(current_user.uuid)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(manager: UserManager, user: UserRegisterInput):
    new_user = User(**user.dict(exclude={"password"}))
    user = await manager.save(new_user, user.password)
    return user
