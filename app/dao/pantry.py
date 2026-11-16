from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.dao.db import get_session
from app.models import PantryItem


def _to_dict(item: PantryItem) -> dict:
    return {
        "id": item.id,
        "ingredient_id": item.ingredient_id,
        "ingredient_name": item.ingredient.name,
        "quantity": float(item.quantity),
        "unit": item.unit,
        "expiry_date": item.expiry_date,
        "added_at": item.added_at,
    }


def list_items(user_id: int) -> list[dict]:
    with get_session() as session:
        query = (
            select(PantryItem)
            .where(PantryItem.user_id == user_id)
            .order_by(PantryItem.expiry_date.asc().nulls_last(), PantryItem.id)
        )
        return [_to_dict(i) for i in session.scalars(query).all()]


def find_by_id(user_id: int, item_id: int) -> dict | None:
    with get_session() as session:
        item = session.get(PantryItem, item_id)
        if item is None or item.user_id != user_id:
            return None
        return _to_dict(item)


def find_by_ingredient(user_id: int, ingredient_id: int) -> dict | None:
    with get_session() as session:
        item = session.scalar(
            select(PantryItem)
            .where(PantryItem.user_id == user_id, PantryItem.ingredient_id == ingredient_id)
            .order_by(PantryItem.id)
        )
        if item is None:
            return None
        return _to_dict(item)


def add_item(user_id: int, ingredient_id: int, quantity: float, unit: str, expiry_date: date | None = None) -> dict:
    with get_session() as session:
        item = PantryItem(
            user_id=user_id,
            ingredient_id=ingredient_id,
            quantity=Decimal(str(quantity)),
            unit=unit,
            expiry_date=expiry_date,
        )
        session.add(item)
        session.flush()
        session.refresh(item)  # load server-generated added_at
        return _to_dict(item)


def update_item(
    user_id: int,
    item_id: int,
    quantity: float | None = None,
    unit: str | None = None,
    expiry_date: date | None = None,
) -> dict | None:
    with get_session() as session:
        item = session.get(PantryItem, item_id)
        if item is None or item.user_id != user_id:
            return None
        if quantity is not None:
            item.quantity = Decimal(str(quantity))
        if unit is not None:
            item.unit = unit
        if expiry_date is not None:
            item.expiry_date = expiry_date
        return _to_dict(item)


def delete_item(user_id: int, item_id: int) -> bool:
    with get_session() as session:
        item = session.get(PantryItem, item_id)
        if item is None or item.user_id != user_id:
            return False
        session.delete(item)
        return True

def ingredient_ids(user_id: int) -> set[int]:
    with get_session() as session:
        rows = session.scalars(
            select(PantryItem.ingredient_id)
            .where(PantryItem.user_id == user_id, PantryItem.quantity > 0)
        ).all()
        return set(rows)