from datetime import date, datetime

from pydantic import BaseModel, Field


class PantryItemCreate(BaseModel):
    ingredient: str = Field(min_length=1)
    quantity: float = Field(gt=0)
    unit: str
    expiry_date: date | None = None


class PantryItemUpdate(BaseModel):
    quantity: float | None = Field(default=None, ge=0)
    unit: str | None = None
    expiry_date: date | None = None


class PantryItemResponse(BaseModel):
    id: int
    ingredient_id: int
    ingredient_name: str
    quantity: float
    unit: str
    expiry_date: date | None = None
    added_at: datetime


class IngredientOption(BaseModel):
    id: int
    name: str
    units: list[str]
