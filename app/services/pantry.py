from app.dao import ingredient as ingredient_dao
from app.dao import pantry as pantry_dao
from app.dto.pantry import PantryItemCreate, PantryItemUpdate, PantryItemResponse
from app.services.exceptions import IngredientNotFoundException, PantryItemNotFoundException


def add_item(user_id: int, data: PantryItemCreate) -> PantryItemResponse:
    ingredient = ingredient_dao.find_by_name(data.ingredient)
    if ingredient is None:
        raise IngredientNotFoundException(data.ingredient)
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
