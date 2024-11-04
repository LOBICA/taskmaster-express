from contextlib import asynccontextmanager
from datetime import date
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from taskmaster.ai.dependencies import (
    inject_twilio_client,
    inject_web_chat_agent,
    inject_whatsapp_chat_agent,
)
from taskmaster.app import app
from taskmaster.auth.token import Token, create_access_token
from taskmaster.database.dependencies import inject_db_session
from taskmaster.database.managers import SubscriptionManager, TaskManager, UserManager
from taskmaster.database.models import BaseModel, UserModel
from taskmaster.paypal.dependencies import inject_paypal_client
from taskmaster.schemas.tasks import Task
from taskmaster.schemas.users import User


@pytest.fixture
async def test_db_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    return engine


@pytest.fixture
def sessionmaker(test_db_engine):
    return async_sessionmaker(test_db_engine, expire_on_commit=False)


@pytest.fixture
async def db_session(sessionmaker):
    async with sessionmaker() as session:
        yield session


@pytest.fixture
def mock_twilio_client():
    return Mock()


@pytest.fixture
def test_client(sessionmaker, mock_twilio_client):
    async def override_db_session():
        async with sessionmaker() as session:
            yield session

    def override_paypal_client():
        return AsyncMock()

    def override_twilio_client():
        return mock_twilio_client

    def override_web_chat_agent():
        return AsyncMock()

    def override_whatsapp_chat_agent():
        return AsyncMock()

    app.dependency_overrides[inject_db_session] = override_db_session
    app.dependency_overrides[inject_paypal_client] = override_paypal_client
    app.dependency_overrides[inject_twilio_client] = override_twilio_client
    app.dependency_overrides[inject_web_chat_agent] = override_web_chat_agent
    app.dependency_overrides[inject_whatsapp_chat_agent] = override_whatsapp_chat_agent

    return TestClient(app)


@pytest.fixture
def admin_user_password():
    return "12345678"


@pytest.fixture
async def test_admin_user(db_session, admin_user_password):
    user = UserModel(email="admin@example.com", name="admin")
    user.set_password(admin_user_password)
    db_session.add(user)
    await db_session.commit()

    return User.model_validate(user)


@pytest.fixture
def test_admin_token(test_admin_user):
    token = create_access_token(Token.create_with_username(test_admin_user.uuid))
    return token


@pytest.fixture
def test_admin_client(test_client: TestClient, test_admin_token):
    test_client.headers["authorization"] = f"Bearer {test_admin_token}"
    return test_client


@pytest.fixture
def user_manager(db_session):
    return UserManager(db_session)


@pytest.fixture
def task_manager(db_session):
    return TaskManager(db_session)


@pytest.fixture
def subscription_manager(db_session):
    return SubscriptionManager(db_session)


@pytest.fixture
def task_manager_generator(db_session):
    async def _task_manager_generator():
        yield TaskManager(db_session)

    return asynccontextmanager(_task_manager_generator)


@pytest.fixture
def patch_task_manager(task_manager_generator):
    return patch(
        "taskmaster.ai.tools.TaskManager.start_session", task_manager_generator
    )


@pytest.fixture
def due_date():
    return date.today().isoformat()


@pytest.fixture
def task_factory(due_date):
    def _task_factory(user: User, n=1):
        tasks = []
        for i in range(n):
            tasks.append(
                Task(
                    title=f"task {i}",
                    user_id=user.uuid,
                    due_date=due_date,
                )
            )
        return tasks

    return _task_factory
