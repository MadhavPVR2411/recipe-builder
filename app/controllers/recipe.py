from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status

from app.controllers.deps import get_optional_user
from app.dto.recipe import RecipeDetail, RecipeSummary
from app.services import recipe as service
from app.services.exceptions import RecipeNotFoundException

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=list[RecipeSummary])
def list_recipes(
    diet_type: Literal["veg", "egg", "non_veg"] | None = None,
    cuisine: str | None = None,
) -> list[RecipeSummary]:
    return service.list_recipes(diet_type, cuisine)


@router.get("/{recipe_id}", response_model=RecipeDetail)
def get_recipe(
    recipe_id: int, user: dict | None = Depends(get_optional_user)
) -> RecipeDetail:
    try:
        return service.get_recipe(recipe_id, user["id"] if user else None)
    except RecipeNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )
