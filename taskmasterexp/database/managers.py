from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Self
from uuid import UUID

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import true

from taskmasterexp.database.connection import get_engine, get_session
from taskmasterexp.schemas.subscriptions import Subscription
from taskmasterexp.schemas.tasks import Task
from taskmasterexp.schemas.users import User

from .models import SubscriptionModel, TaskModel, UserModel


class BaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    @asynccontextmanager
    async def start_session(cls) -> AsyncGenerator[Self, Any]:
        async with get_engine() as engine:
            async with get_session(engine) as session:
                yield cls(session)


class UserManager(BaseManager):
    async def list(self) -> list[User]:
        stmt = select(UserModel)
        result: Result = await self.session.execute(stmt)
        return [User.from_orm(model) for model in result.scalars()]

    async def get(self, user_id: UUID) -> User | None:
        model = await self.session.get(UserModel, user_id)
        if model:
            return User.from_orm(model)

        return None

    async def get_by_phone(self, phone_number: str) -> User | None:
        stmt = select(UserModel).where(UserModel.phone_number == phone_number)
        result: Result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return User.from_orm(model)

        return None

    async def save(self, user: User, password: str = None) -> User:
        if user.uuid:
            model = await self.session.get(UserModel, user.uuid)
            for field, value in user.dict().items():
                setattr(model, field, value)
        else:
            model = UserModel(**user.dict(exclude={"uuid"}))
            self.session.add(model)

        if password:
            model.set_password(password)

        await self.session.commit()
        await self.session.refresh(model)
        return User.from_orm(model)

    async def change_password(
        self, user_id: UUID, password: str, new_password: str
    ) -> None:
        model = await self.session.get(UserModel, user_id)
        if model:
            if model.verify_password(password):
                model.set_password(new_password)
                await self.session.commit()
            else:
                raise ValueError("Invalid password")

    async def _merge_users(
        self, primary_user: UserModel, secondary_user: UserModel
    ) -> None:
        if not primary_user.email:
            primary_user.email = secondary_user.email
            secondary_user.email = None

        if not primary_user.password:
            primary_user.password = secondary_user.password

        if not primary_user.phone_number:
            primary_user.phone_number = secondary_user.phone_number
            secondary_user.phone_number = None

        if not primary_user.fb_user_id:
            primary_user.fb_user_id = secondary_user.fb_user_id
            secondary_user.fb_user_id = None

        tasks: list[TaskModel] = await secondary_user.awaitable_attrs.tasks
        for task in tasks:
            task.user_id = primary_user.uuid

        secondary_user.disabled = True

        await self.session.commit()

    async def merge_users(self, primary_user_id: UUID, secondary_user_id: UUID) -> None:
        primary_user = await self.session.get(UserModel, primary_user_id)
        secondary_user = await self.session.get(UserModel, secondary_user_id)
        if primary_user and secondary_user:
            await self._merge_users(primary_user, secondary_user)

    async def associate_email(self, user_id: UUID, email: str) -> None:
        user = await self.session.get(UserModel, user_id)

        if user is None or user.email:
            raise Exception("User not found or already has an email")

        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user and user:
            await self._merge_users(user, existing_user)
        elif user:
            user.email = email
            await self.session.commit()

    async def delete(self, user_id: UUID) -> None:
        model = await self.session.get(UserModel, user_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()


class TaskManager(BaseManager):
    async def list(self, params: dict = None) -> list[Task]:
        stmt = select(TaskModel)
        if params:
            if "user_id" in params:
                stmt = stmt.where(TaskModel.user_id == params["user_id"])
            if "status" in params:
                stmt = stmt.where(TaskModel.status == params["status"])
        result: Result = await self.session.execute(stmt)
        return [Task.from_orm(model) for model in result.scalars()]

    async def get(self, task_id: UUID) -> Task | None:
        model = await self.session.get(TaskModel, task_id)
        if model:
            return Task.from_orm(model)

        return None

    async def save(self, task: Task) -> Task:
        if task.uuid:
            model = await self.session.get(TaskModel, task.uuid)
            for field, value in task.dict().items():
                setattr(model, field, value)
        else:
            model = TaskModel(**task.dict(exclude={"uuid"}))
            self.session.add(model)

        await self.session.commit()
        await self.session.refresh(model)
        return Task.from_orm(model)

    async def delete(self, task_id: UUID) -> None:
        model = await self.session.get(TaskModel, task_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()


class SubscriptionManager(BaseManager):
    async def get_subscription_by_subscription_id(
        self, subscription_id: str
    ) -> Subscription | None:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.subscription_id == subscription_id
        )
        results = await self.session.execute(stmt)
        model = results.scalar_one_or_none()
        if model:
            return Subscription.from_orm(model)

        return None

    async def link_subscription(
        self, user_id: UUID, subscription_id: str
    ) -> Subscription:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.subscription_id == subscription_id
        )
        results = await self.session.execute(stmt)
        subscription = results.scalar_one_or_none()
        if subscription:
            subscription.user_id = user_id
        else:
            subscription = SubscriptionModel(
                user_id=user_id, subscription_id=subscription_id, is_active=False
            )
            self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)
        return Subscription.from_orm(subscription)

    async def activate_subscription(
        self, subscription_id: str, plan_id: str
    ) -> Subscription:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.subscription_id == subscription_id
        )
        results = await self.session.execute(stmt)
        subscription = results.scalar_one_or_none()
        if subscription:
            subscription.is_active = True
            subscription.plan_id = plan_id
        else:
            subscription = SubscriptionModel(
                subscription_id=subscription_id, is_active=True, plan_id=plan_id
            )
            self.session.add(subscription)

        await self.session.commit()
        await self.session.refresh(subscription)
        return Subscription.from_orm(subscription)

    async def cancel_subscription(self, subscription_id: str) -> None:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.subscription_id == subscription_id,
            SubscriptionModel.is_active == true(),
        )
        results = await self.session.execute(stmt)
        subscription = results.scalar_one_or_none()
        if subscription:
            subscription.is_active = False
            await self.session.commit()

    async def get_active_subscription(self, user_id: UUID) -> Subscription | None:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.user_id == user_id,
            SubscriptionModel.is_active == true(),
        )
        results = await self.session.execute(stmt)
        model = results.scalar_one_or_none()
        if model:
            return Subscription.from_orm(model)

        return None
