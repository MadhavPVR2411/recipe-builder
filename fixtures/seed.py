import json
from pathlib import Path

from sqlalchemy import select

from app.dao.db import get_session
from app.models import Ingredient, Recipe, RecipeIngredient, RecipeStep

HERE = Path(__file__).parent
RECIPE_FIELDS = ["name", "cuisine", "serving", "prep_time", "cook_time",
                 "total_time", "step_count", "diet_type", "complexity"]


def main() -> None:
    ingredients = json.loads((HERE / "ingredients.json").read_text())
    recipes = json.loads((HERE / "recipes.json").read_text())

    with get_session() as session:
        if session.scalar(select(Recipe).limit(1)) is not None:
            print("Recipes already seeded, skipping.")
            return

        by_name = {}
        for i in ingredients:
            ingredient = Ingredient(name=i["name"], diet=i["diet"], unit_kind=i["unit_kind"])
            session.add(ingredient)
            by_name[i["name"]] = ingredient

        for r in recipes:
            recipe = Recipe(**{field: r[field] for field in RECIPE_FIELDS})
            for i in r["ingredients"]:
                recipe.ingredients.append(
                    RecipeIngredient(ingredient=by_name[i["name"]], quantity=i["quantity"], unit=i["unit"])
                )
            for number, text in enumerate(r["steps"], start=1):
                recipe.steps.append(RecipeStep(step_number=number, instruction=text))
            session.add(recipe)

    print(f"Seeded {len(ingredients)} ingredients and {len(recipes)} recipes.")


if __name__ == "__main__":
    main()