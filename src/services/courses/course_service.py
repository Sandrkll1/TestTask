from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.models.courses import Course, Category
from src.services.CRUD import BaseCRUD


class CourseService(BaseCRUD):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(Course, Course.id.key, session_factory)

    async def get_categories(self) -> list[Category]:
        async with self.session_factory() as session:
            result = await session.execute(select(Category))
            return result.scalars().all()

    async def get_courses(self, limit: int = 20, offset: int = 0) -> list[Course]:
        async with self.session_factory() as session:
            result = await session.execute(select(Course).limit(limit).offset(offset))
            return result.unique().scalars().all()

    async def get_courses_by_category(
            self,
            category_id: int,
            limit: int = 20,
            offset: int = 0
    ) -> list[Course]:
        async with self.session_factory() as session:
            query = (
                select(Course)
                .join(Course.categories)
                .where(Category.id == category_id)
                .options(selectinload(Course.categories))
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def search_courses(
            self,
            search_term: str,
            limit: int = 20,
            offset: int = 0
    ) -> list[Course]:
        async with self.session_factory() as session:
            query = (
                select(Course)
                .where(Course.title.ilike(f"%{search_term}%"))
                .options(selectinload(Course.categories))
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
