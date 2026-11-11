from sqlalchemy import select

from app.dao.db import get_session
from app.models import Recipe


def _summary(recipe: Recipe) -> dict:
    return {
        "id": recipe.id,
        "name": recipe.name,
        "cuisine": recipe.cuisine,
        "total_time": recipe.total_time,
        "diet_type": recipe.diet_type,
        "complexity": recipe.complexity,
    }


def list_recipes(diet_type: str | None = None, cuisine: str | None = None) -> list[dict]:
    with get_session() as session:
        query = select(Recipe).order_by(Recipe.name)
        if diet_type is not None:
            query = query.where(Recipe.diet_type == diet_type)
        if cuisine is not None:
            query = query.where(Recipe.cuisine == cuisine)
        return [_summary(r) for r in session.scalars(query).all()]


def find_by_id(recipe_id: int) -> dict | None:
    with get_session() as session:
        recipe = session.get(Recipe, recipe_id)
        if recipe is None:
            return None
        return {
            **_summary(recipe),
            "serving": recipe.serving,
            "prep_time": recipe.prep_time,
            "cook_time": recipe.cook_time,
            "ingredients": [
                {"name": ri.ingredient.name, "quantity": float(ri.quantity), "unit": ri.unit}
                for ri in recipe.ingredients
            ],
            "steps": [step.instruction for step in recipe.steps],
        }