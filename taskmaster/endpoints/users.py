from fastapi import APIRouter, HTTPException, status

from taskmaster.auth.dependencies import CurrentUser
from taskmaster.database.dependencies import UserManager
from taskmaster.schemas.users import (
    PasswordInput,
    User,
    UserRegisterInput,
    UserResponse,
)

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: CurrentUser):
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(manager: UserManager, current_user: CurrentUser):
    await manager.delete(current_user.uuid)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(manager: UserManager, user: UserRegisterInput):
    new_user = User(**user.model_dump(exclude={"password"}))
    user = await manager.save(new_user, user.password)
    return user


@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    manager: UserManager,
    current_user: CurrentUser,
    data: PasswordInput,
):
    try:
        await manager.change_password(
            current_user.uuid, data.password, data.new_password
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
