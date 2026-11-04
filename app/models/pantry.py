from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Text, Numeric, Date, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PantryItem(Base):
    __tablename__ = "pantry_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredient.id", ondelete="RESTRICT"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    unit: Mapped[str] = mapped_column(Text)
    expiry_date: Mapped[date| None] = mapped_column(Date)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ingredient: Mapped["Ingredient"] = relationship()

    __table_args__ = (CheckConstraint("quantity >= 0", name="ck_pantry_item_quantity"),)