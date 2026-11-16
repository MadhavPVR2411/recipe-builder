from app.dao import ingredient as ingredient_dao
from app.dao import pantry as pantry_dao
from app.dto.pantry import PantryItemCreate, PantryItemUpdate, PantryItemResponse, IngredientOption
from app.services.exceptions import IngredientNotFoundException, PantryItemNotFoundException
from app.services.exceptions import InvalidUnitException

UNITS = {
    "weight": ["g","kg"],
    "volume": ["ml","litre"],
    "count":  ["pcs"],
}

# how many base units (g, ml, pcs) one of each unit is worth
TO_BASE = {"g": 1, "kg": 1000, "ml": 1, "litre": 1000, "pcs": 1}


def _earliest(*dates):
    dates = [d for d in dates if d is not None]
    return min(dates) if dates else None


def add_item(user_id: int, data: PantryItemCreate) -> PantryItemResponse:
    ingredient = ingredient_dao.find_by_name(data.ingredient)
    if ingredient is None:
        raise IngredientNotFoundException(data.ingredient)
    allowed = UNITS[ingredient["unit_kind"]]
    if data.unit not in allowed:
        raise InvalidUnitException(data.unit, allowed)

    # already in the pantry: top up the existing item instead of adding a second row
    existing = pantry_dao.find_by_ingredient(user_id, ingredient["id"])
    if existing is not None and existing["unit"] in TO_BASE:
        added = data.quantity * TO_BASE[data.unit] / TO_BASE[existing["unit"]]
        item = pantry_dao.update_item(
            user_id,
            existing["id"],
            quantity=round(existing["quantity"] + added, 3),
            expiry_date=_earliest(existing["expiry_date"], data.expiry_date),
        )
        return PantryItemResponse(**item)

    item = pantry_dao.add_item(
        user_id,
        ingredient["id"],
        data.quantity,
        data.unit,
        data.expiry_date,
    )
    return PantryItemResponse(**item)


def list_items(user_id: int) -> list[PantryItemResponse]:
    return [PantryItemResponse(**i) for i in pantry_dao.list_items(user_id)]


def update_item(user_id: int, item_id: int, data: PantryItemUpdate) -> PantryItemResponse:
    item = pantry_dao.update_item(user_id, item_id, data.quantity, data.unit, data.expiry_date)
    if item is None:
        raise PantryItemNotFoundException(item_id)
    return PantryItemResponse(**item)


def delete_item(user_id: int, item_id: int) -> None:
    if not pantry_dao.delete_item(user_id, item_id):
        raise PantryItemNotFoundException(item_id)

def list_ingredient_options() -> list[IngredientOption]:
    return [
        IngredientOption(id=i["id"], name=i["name"], units=UNITS[i["unit_kind"]])
        for i in ingredient_dao.list_all()
    ]

