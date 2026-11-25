from app.dao import pantry as pantry_dao
from app.dao import recipe as recipe_dao
from app.dto.recipe import RecipeDetail, RecipeSummary
from app.services.exceptions import RecipeNotFoundException


def list_recipes(
    diet_type: str | None = None, cuisine: str | None = None
) -> list[RecipeSummary]:
    return [RecipeSummary(**r) for r in recipe_dao.list_recipes(diet_type, cuisine)]


def get_recipe(recipe_id: int, user_id: int | None = None) -> RecipeDetail:
    recipe = recipe_dao.find_by_id(recipe_id)
    if recipe is None:
        raise RecipeNotFoundException(recipe_id)
    if user_id is not None:
        have = pantry_dao.ingredient_ids(user_id)
        for ingredient in recipe["ingredients"]:
            ingredient["in_pantry"] = ingredient["ingredient_id"] in have
    return RecipeDetail(**recipe)
