from sqlalchemy import select

from app.dao.db import get_session
from app.models import Ingredient


def find_by_name(name: str) -> dict | None:
    with get_session() as session:
        ingredient = session.scalar(
            select(Ingredient).where(Ingredient.name == name.strip().lower())
        )
        if ingredient is None:
            return None
        return {
            "id": ingredient.id,
            "name": ingredient.name,
            "unit_kind": ingredient.unit_kind,
        }


def list_all() -> list[dict]:
    with get_session() as session:
        ingredients = session.scalars(
            select(Ingredient).order_by(Ingredient.name.asc())
        )
        return [
            {"id": i.id, "name": i.name, "unit_kind": i.unit_kind} for i in ingredients
        ]
