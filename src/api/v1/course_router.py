from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from dependency_injector.wiring import Provide, inject

from src.di import Container

from src.models.user import User
from src.repositories.course_repository import CourseRepository
from src.schemas.course import Category, Course, UserFavorite
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/courses")


@router.get("/categories", response_model=list[Category])
@cache(expire=30)
@inject
async def get_categories(
        course_repository: CourseRepository = Depends(Provide[Container.course_repository]),
        user: User = Depends(get_current_user)
):
    return await course_repository.get_categories()


@router.get("/", response_model=list[Course])
@cache(expire=30)
@inject
async def get_courses(
        category_id: int | None = None,
        search_query: str | None = None,
        limit: int = 20,
        offset: int = 0,
        course_repository: CourseRepository = Depends(Provide[Container.course_repository]),
        user: User = Depends(get_current_user)
):
    return await course_repository.get_courses(
        user_id=user.id,
        category_id=category_id,
        search_query=search_query,
        limit=limit,
        offset=offset
    )


@router.post("/favorites", response_model=Course)
@inject
async def toggle_favorite(
        favorite: UserFavorite,
        course_repository: CourseRepository = Depends(Provide[Container.course_repository]),
        user: User = Depends(get_current_user)
):
    return await course_repository.toggle_favorite(user_id=user.id, favorite=favorite)


@router.get("/favorites", response_model=list[Course])
@cache(expire=30)
@inject
async def get_user_favorites(
        limit: int = 20,
        offset: int = 0,
        course_repository: CourseRepository = Depends(Provide[Container.course_repository]),
        user: User = Depends(get_current_user)
):
    return await course_repository.get_user_favorites(user_id=user.id, limit=limit, offset=offset)


@router.get("/{course_id}", response_model=Course)
@inject
async def course_details(
        course_id: int,
        course_repository: CourseRepository = Depends(Provide[Container.course_repository]),
        user: User = Depends(get_current_user)
):
    ...  # to do
