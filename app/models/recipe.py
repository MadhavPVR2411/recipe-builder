from decimal import Decimal

from sqlalchemy import Text, Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Ingredient(Base):
    __tablename__ = "ingredient"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(Text, unique=True)
    diet: Mapped[str] = mapped_column(Text)
    unit_kind: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("diet IN ('veg', 'egg', 'non_veg')", name="ck_ingredient_diet"),
        CheckConstraint("unit_kind IN ('count', 'weight', 'volume')", name="ck_ingredient_unit_kind"),
    )


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)
    cuisine: Mapped[str] = mapped_column(Text)
    serving: Mapped[int] = mapped_column(Integer)
    prep_time: Mapped[int] = mapped_column(Integer)
    cook_time: Mapped[int] = mapped_column(Integer)
    total_time: Mapped[int] = mapped_column(Integer)
    step_count: Mapped[int] = mapped_column(Integer)
    diet_type: Mapped[str] = mapped_column(Text)
    complexity: Mapped[str] = mapped_column(Text)

    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe", cascade="all, delete-orphan"
    )
    steps: Mapped[list["RecipeStep"]] = relationship(
        back_populates="recipe", cascade="all, delete-orphan", order_by="RecipeStep.step_number"
    )

    __table_args__ = (
        CheckConstraint("serving > 0", name="ck_recipe_serving"),
        CheckConstraint("prep_time >= 0", name="ck_recipe_prep_time"),
        CheckConstraint("cook_time >= 0", name="ck_recipe_cook_time"),
        CheckConstraint("total_time > 0", name="ck_recipe_total_time"),
        CheckConstraint("step_count > 0", name="ck_recipe_step_count"),
        CheckConstraint("diet_type IN ('veg', 'egg', 'non_veg')", name="ck_recipe_diet_type"),
        CheckConstraint("complexity IN ('easy', 'medium', 'hard')", name="ck_recipe_complexity"),
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id", ondelete="CASCADE"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.id", ondelete="RESTRICT"), primary_key=True
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    unit: Mapped[str] = mapped_column(Text)

    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship()

    __table_args__ = (CheckConstraint("quantity > 0", name="ck_recipe_ingredient_quantity"),)


class RecipeStep(Base):
    __tablename__ = "recipe_steps"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id", ondelete="CASCADE"), primary_key=True
    )
    step_number: Mapped[int] = mapped_column(Integer, primary_key = True)
    instruction: Mapped[str] = mapped_column(Text)

    recipe: Mapped["Recipe"] = relationship(back_populates="steps")