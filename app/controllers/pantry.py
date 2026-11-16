from fastapi import APIRouter, Depends, HTTPException, status

from app.controllers.deps import get_current_user
from app.dto.pantry import PantryItemCreate, PantryItemUpdate, PantryItemResponse, IngredientOption
from app.services import pantry as service
from app.services.exceptions import IngredientNotFoundException, PantryItemNotFoundException

router = APIRouter(prefix="/pantry", tags=["pantry"])


@router.post("", response_model=PantryItemResponse, status_code=status.HTTP_201_CREATED)
def add_item(body: PantryItemCreate, user: dict = Depends(get_current_user)) -> PantryItemResponse:
    try:
        return service.add_item(user["id"], body)
    except IngredientNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")


@router.get("", response_model=list[PantryItemResponse])
def list_items(user: dict = Depends(get_current_user)) -> list[PantryItemResponse]:
    return service.list_items(user["id"])


@router.patch("/{item_id}", response_model=PantryItemResponse)
def update_item(item_id: int, body: PantryItemUpdate, user: dict = Depends(get_current_user)) -> PantryItemResponse:
    try:
        return service.update_item(user["id"], item_id, body)
    except PantryItemNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pantry item not found")


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, user: dict = Depends(get_current_user)) -> None:
    try:
        service.delete_item(user["id"], item_id)
    except PantryItemNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pantry item not found")

@router.get("/ingredients", response_model=list[IngredientOption])
def list_ingredients(user: dict = Depends(get_current_user)) -> list[IngredientOption]:
    return service.list_ingredient_options()