from app.dao import recipe as recipe_dao
from app.dto.recipe import RecipeDetail, RecipeSummary
from app.services.exceptions import RecipeNotFoundException


def list_recipes(
    diet_type: str | None = None, cuisine: str | None = None
) -> list[RecipeSummary]:
    return [RecipeSummary(**r) for r in recipe_dao.list_recipes(diet_type, cuisine)]


def get_recipe(recipe_id: int) -> RecipeDetail:
    recipe = recipe_dao.find_by_id(recipe_id)
    if recipe is None:
        raise RecipeNotFoundException(recipe_id)
    return RecipeDetail(**recipe)
