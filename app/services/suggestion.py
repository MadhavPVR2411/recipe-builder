from app.dao import pantry as pantry_dao
from app.dao import profile as profile_dao
from app.dao import recipe as recipe_dao
from app.dto.recipe import MissingOneSuggestion, RecipeSummary, SuggestionsResponse
from app.services.diet import allowed_diets


def get_suggestions(user_id: int) -> SuggestionsResponse:
    profile = profile_dao.get_profile(user_id)
    diet = profile["diet_type"] if profile is not None else "non_veg"

    pantry_ids = pantry_dao.ingredient_ids(user_id)
    recipes = recipe_dao.list_with_ingredients(allowed_diets(diet))

    can_make = []
    missing_one = []

    for recipe in recipes:
        ingredients = recipe.pop("ingredients")
        missing = set(ingredients) - pantry_ids

        if len(missing) == 0:
            can_make.append(RecipeSummary(**recipe))
        elif len(missing) == 1:
            missing_id = next(iter(missing))
            missing_one.append(
                MissingOneSuggestion(
                    **recipe, missing_ingredient=ingredients[missing_id]
                )
            )

    return SuggestionsResponse(can_make=can_make, missing_one=missing_one)
