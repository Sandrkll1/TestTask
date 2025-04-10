from src.models.base import Base

from sqlalchemy import Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, time


class Category(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    courses: Mapped[list["Course"]] = relationship(
        secondary="CourseCategory",
        back_populates="categories"
    )


class Course(Base):
    __tablename__ = "Courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[time] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[time] = mapped_column(DateTime(timezone=True), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    provided: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    categories: Mapped[list["Category"]] = relationship(
        secondary="CourseCategory",
        back_populates="courses",
        lazy="joined"
    )


class CourseCategory(Base):
    __tablename__ = "CourseCategory"

    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("Courses.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("Categories.id"), primary_key=True)


class UserFavorite(Base):
    __tablename__ = "UserFavorite"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("User.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("Courses.id"), primary_key=True)
