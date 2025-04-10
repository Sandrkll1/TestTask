from contextlib import AbstractContextManager
from typing import Any, Callable, Type

from sqlalchemy import select
from sqlalchemy.orm import Session


class BaseCRUD:
    def __init__(self,
                 model_class: Type,
                 primary_key: int | str,
                 session_factory: Callable[..., AbstractContextManager[Session]]):
        self.model_class = model_class
        self.primary_key = primary_key
        self.session_factory = session_factory

    async def create(self, **kwargs) -> Any:
        async with self.session_factory() as session:
            obj = self.model_class(**kwargs)
            session.add(obj)
            await session.flush()
            await session.refresh(obj)
            return obj

    async def get(self, primary_key_value: int | str) -> Any:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model_class).where(getattr(self.model_class, self.primary_key) == primary_key_value))
            return result.scalars().first()

    async def update(self, primary_key_value: int | str, new_data: dict = None, **kwargs) -> Any:
        new_data = kwargs if new_data is None else new_data
        async with self.session_factory() as session:
            stmt = await session.execute(
                select(self.model_class).where(getattr(self.model_class, self.primary_key) == primary_key_value))
            obj = stmt.scalars().first()
            if obj:
                for key, value in new_data.items():
                    setattr(obj, key, value)
                await session.flush()
                await session.refresh(obj)
                return obj

    async def delete(self, primary_key_value: int | str) -> bool:
        async with self.session_factory() as session:
            query = select(self.model_class).where(getattr(self.model_class, self.primary_key) == primary_key_value)
            result = await session.execute(query)
            obj = result.scalars().first()
            if obj:
                await session.delete(obj)
                return True
            return False
