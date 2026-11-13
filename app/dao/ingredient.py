from sqlalchemy import select
from app.models import Ingredient
from app.dao.db import get_session


def find_by_name(name: str) -> dict | None:
    with get_session() as session:
        ingredient = session.scalar(select(Ingredient).where(Ingredient.name == name.strip().lower()))
        if ingredient is None:
            return None
        return {"id": ingredient.id, "name": ingredient.name}
