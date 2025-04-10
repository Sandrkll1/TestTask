from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user.user import User
from src.services.CRUD import BaseCRUD


class UserService(BaseCRUD):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super(UserService, self).__init__(User, User.id.key, session_factory)

    async def get(self, user_id: int = None, email: str = None) -> User:
        async with self.session_factory() as session:
            if user_id:
                result = await session.execute(select(User).where(User.id == user_id))
                return result.scalars().first()
            elif email:
                result = await session.execute(select(User).where(User.email == email))
                return result.scalars().first()
