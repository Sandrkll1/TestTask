from datetime import datetime

from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str


class CourseBase(BaseModel):
    title: str
    image_url: str
    start_time: datetime
    end_time: datetime
    duration: int
    location: str
    provided: str
    date: datetime
    description: str | None = None


class Course(CourseBase):
    id: int
    categories: list[Category]
    is_favorite: bool | None = None


class UserFavorite(BaseModel):
    course_id: int
