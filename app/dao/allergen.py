from sqlalchemy import select

from app.dao.db import get_session
from app.models import Allergen


def list_all() -> list[dict]:
    with get_session() as session:
        allergens = session.scalars(select(Allergen).order_by(Allergen.name)).all()
        return [{"id": a.id, "name": a.name} for a in allergens]


def find_by_id(allergen_id: int) -> dict | None:
    with get_session() as session:
        allergen = session.get(Allergen, allergen_id)
        if allergen is None:
            return None
        return {"id": allergen.id, "name": allergen.name}