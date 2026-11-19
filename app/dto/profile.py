from typing import Literal

from pydantic import BaseModel


class AllergenResponse(BaseModel):
    id: int
    name: str


class ProfileResponse(BaseModel):
    diet_type: str
    allergens: list[AllergenResponse]


class DietUpdateRequest(BaseModel):
    diet_type: Literal["veg", "egg", "non_veg"]
