from datetime import datetime

from sqlalchemy import Text, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(Text, unique=True)
    password_hash: Mapped[str] = mapped_column(Text)


class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    diet_type: Mapped[str] = mapped_column(Text, server_default="veg")
    last_login_at: Mapped[datetime |None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("diet_type IN ('veg', 'egg', 'non_veg')", name="ck_user_profile_diet_type"),
    )