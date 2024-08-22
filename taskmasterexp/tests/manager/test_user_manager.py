from taskmasterexp.database.managers import UserManager
from taskmasterexp.schemas.users import User


async def test_user_manager(user_manager: UserManager):
    users = await user_manager.list()
    assert users == []

    new_user = User(name="test", email="test@example.com")

    user = await user_manager.save(new_user)
    assert user.email == new_user.email

    users = await user_manager.list()
    assert users == [user]

    user_ = await user_manager.get(user.uuid)
    assert user == user_

    user_.name = "update name"
    user = await user_manager.save(user_)
    assert user.name == "update name"

    await user_manager.delete(user.uuid)
    users = await user_manager.list()
    assert users == []
    user_ = await user_manager.get(user.uuid)
    assert user_ is None
