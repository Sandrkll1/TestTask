from datetime import datetime

from sqlalchemy import TIMESTAMP, BigInteger, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Auth(Base):
    __tablename__ = "Auth"

    refresh_token: Mapped[str] = mapped_column(Text, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("User.id"), nullable=False)
    denied: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
