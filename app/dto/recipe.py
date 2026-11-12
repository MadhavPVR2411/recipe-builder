from typing import List

from pydantic import BaseModel


class RecipeSummary(BaseModel):
    id: int
    name: str
    cuisine: str
    total_time: int
    diet_type: str
    complexity: str

class RecipeIngredientResponse(BaseModel):
    name: str
    quantity: float
    unit: str

class RecipeDetail(RecipeSummary):
  serving: int
  prep_time: int
  cook_time: int
  ingredients: List[RecipeIngredientResponse]
  steps: list[str]

