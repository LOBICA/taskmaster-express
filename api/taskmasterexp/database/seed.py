import asyncio

from .connection import get_engine, get_session
from .models import UserModel


async def seed():
    user = UserModel(email="admin@example.com", name="Admin")
    user.set_password("password")

    async with get_engine() as engine:
        async with get_session(engine) as session:
            session.add(user)
            await session.commit()


if __name__ == "__main__":
    print("Seeding database...")
    asyncio.run(seed())
    print("Done!")
