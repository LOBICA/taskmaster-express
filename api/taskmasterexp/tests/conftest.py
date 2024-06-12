import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from taskmasterexp.app import app
from taskmasterexp.auth.token import TokenData, create_access_token
from taskmasterexp.database.dependencies import inject_db_session
from taskmasterexp.database.managers import TaskManager
from taskmasterexp.database.models import BaseModel, UserModel
from taskmasterexp.schemas.tasks import Task
from taskmasterexp.schemas.users import User


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
def test_client(sessionmaker):
    async def override_db_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[inject_db_session] = override_db_session
    return TestClient(app)


@pytest.fixture
def admin_user_password():
    return "12345678"


@pytest.fixture
async def test_admin_user(db_session, admin_user_password):
    user = UserModel(email="admin@example.com")
    user.set_password(admin_user_password)
    db_session.add(user)
    await db_session.commit()

    return User.from_orm(user)


@pytest.fixture
def test_admin_token(test_admin_user):
    token = create_access_token(TokenData.create_with_username(test_admin_user.uuid))
    return token


@pytest.fixture
def test_admin_client(test_client: TestClient, test_admin_token):
    test_client.headers["authorization"] = f"Bearer {test_admin_token}"
    return test_client


@pytest.fixture
def task_manager(db_session):
    return TaskManager(db_session)


@pytest.fixture
def task_factory():
    def _task_factory(user: User, n=1):
        tasks = []
        for i in range(n):
            tasks.append(
                Task(
                    title=f"task {i}",
                    user_id=user.uuid,
                )
            )
        return tasks

    return _task_factory
