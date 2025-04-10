from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import and_, select, update
from sqlalchemy.orm import Session

from src.models.user import Auth
from src.services.CRUD import BaseCRUD


class AuthService(BaseCRUD):

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        super(AuthService, self).__init__(Auth, Auth.refresh_token.key, session_factory)

    async def get(self, user_id: int = None, refresh_token: str = None) -> Auth:
        async with self.session_factory() as session:
            if user_id:
                stmt = await session.execute(select(Auth).where(and_(Auth.user_id == user_id, Auth.denied == False)))
            elif refresh_token:
                stmt = await session.execute(select(Auth).where(Auth.refresh_token == refresh_token))
            return stmt.scalars().first()

    async def mark_denied(self, refresh_token: str) -> Auth:
        async with self.session_factory() as session:
            stmt = select(Auth).where(Auth.refresh_token == refresh_token)

            result = await session.execute(stmt)
            obj = result.scalars().first()
            if obj:
                obj.denied = True
                await session.flush()
                return obj

    async def mark_all_denied(self, user_id: int):
        async with self.session_factory() as session:
            await session.execute(
                update(Auth)
                .where(Auth.user_id == user_id)
                .values(denied=True)
            )
            await session.commit()
