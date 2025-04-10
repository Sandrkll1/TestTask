from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import and_, select
from sqlalchemy.orm import Session, selectinload

from src.models.courses import Course, UserFavorite


class FavoriteService:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    async def toggle_favorite(self, user_id: int, course_id: int) -> tuple[Course, bool] | None:
        async with self.session_factory() as session:
            query = select(Course).where(Course.id == course_id)
            course = await session.execute(query)
            course = course.unique().scalars().one_or_none()
            if not course:
                return None

            query = select(UserFavorite).where(
                and_(
                    UserFavorite.user_id == user_id,
                    UserFavorite.course_id == course_id
                )
            )
            existing = await session.execute(query)
            existing = existing.scalars().first()

            if existing:
                await session.delete(existing)
                await session.commit()
                return course, False
            else:
                favorite = UserFavorite(user_id=user_id, course_id=course_id)
                session.add(favorite)
                await session.commit()
                return course, True

    async def is_favorite(self, user_id: int, course_id: int) -> bool:
        async with self.session_factory() as session:
            query = select(UserFavorite).where(
                and_(
                    UserFavorite.user_id == user_id,
                    UserFavorite.course_id == course_id
                )
            )
            result = await session.execute(query)
            return result.scalars().first() is not None

    async def get_user_favorites(self, user_id: int, limit: int = 20, offset: int = 0) -> list[Course]:
        async with self.session_factory() as session:
            query = (
                select(Course)
                .join(UserFavorite, UserFavorite.course_id == Course.id)
                .where(UserFavorite.user_id == user_id)
                .options(selectinload(Course.categories))
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            return result.scalars().all()
