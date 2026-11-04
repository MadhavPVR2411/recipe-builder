from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.models.base import Base


class Allergen(Base):
    __tablename__ = "allergen"
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(Text, unique=True)
    users: Mapped[list["User"]] = relationship(
        secondary="user_allergen",
        back_populates="allergens",
    )