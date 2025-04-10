from src.services.courses import CourseService, FavoriteService
from src.schemas.course import Category, Course, UserFavorite


class CourseRepository:

    def __init__(
            self,
            course_service: CourseService,
            favorite_service: FavoriteService
    ):
        self.course_service = course_service
        self.favorite_service = favorite_service

    async def get_categories(self) -> list[Category]:
        categories = await self.course_service.get_categories()
        return [
            Category.model_validate(category, from_attributes=True)
            for category in categories
        ]

    async def get_courses(
            self,
            user_id: int,
            category_id: int | None = None,
            search_query: str | None = None,
            limit: int = 20,
            offset: int = 0
    ) -> list[Course]:

        if search_query:
            courses = await self.course_service.get_courses_by_category(
                category_id=category_id,
                limit=limit,
                offset=offset
            )
        elif search_query:
            courses = await self.course_service.search_courses(
                search_term=search_query,
                limit=limit,
                offset=offset
            )
        else:
            courses = await self.course_service.get_courses(
                limit=limit,
                offset=offset
            )

        return [
            Course.model_validate(course, from_attributes=True)
            for course in courses
            if setattr(course, "is_favorite", await self.favorite_service.is_favorite(user_id, course.id)) or True
        ]

    async def toggle_favorite(self, user_id: int, favorite: UserFavorite) -> Course:
        course, is_favorite = await self.favorite_service.toggle_favorite(
            user_id=user_id,
            course_id=favorite.course_id
        )
        course.is_favorite = is_favorite
        return Course.model_validate(course, from_attributes=True)

    async def get_user_favorites(self, user_id: int, limit: int = 20, offset: int = 0) -> list[Course]:
        favorites = await self.favorite_service.get_user_favorites(user_id=user_id, limit=limit, offset=offset)
        return [
            Course.model_validate(course, from_attributes=True)
            for course in favorites
            if setattr(course, "is_favorite", True) or True
        ]
