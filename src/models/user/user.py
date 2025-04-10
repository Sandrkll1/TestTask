from datetime import datetime

from sqlalchemy import TEXT, TIMESTAMP, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(TEXT, nullable=False)

    register_timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    last_seen_timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
