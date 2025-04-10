from fastapi import APIRouter, FastAPI

from src.api.v1.auth_router import router as auth_router
from src.api.v1.course_router import router as course_router


def setup(app: FastAPI):
    router = APIRouter(prefix="/v1")

    router.include_router(auth_router)
    router.include_router(course_router)

    app.include_router(router)
