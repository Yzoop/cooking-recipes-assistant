from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field


class Unit(StrEnum):
    PIECE = "piece"
    ML = "ml"
    L = "l"
    MG = "mg"
    G = "g"
    KG = "kg"


class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient.")
    quantity: float | None = Field(None, description="Quantity of the ingredient.")
    unit: Unit | None = Field(None, description="Unit of measurement (e.g., piece, ml, g).")


class DishInfo(BaseModel):
    calories: int | None = Field(None, description="Calories per serving.")
    prep_time: int | None = Field(None, description="Preparation time in minutes.")
    cook_time: int | None = Field(None, description="Cooking time in minutes.")
    total_time: int | None = Field(None, description="Total time in minutes (auto-calculated).")


class Recipe(BaseModel):
    title: str = Field(..., description="Title of the recipe.")
    ingredients: list[Ingredient] = Field(..., description="List of ingredients.")
    steps: List[str] = Field(..., description="Step-by-step instructions.")
    dish_info: DishInfo | None = Field(None, description="Additional information about the dish.")
    tags: List[str] | None = Field(None, description="Tags for categorizing the recipe.")
