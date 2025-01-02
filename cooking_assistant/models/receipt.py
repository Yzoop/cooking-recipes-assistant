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


class Language(StrEnum):
    UKRAINIAN = "uk"
    ENGLISH = "en"
    BELARUSIAN = "by"


class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient.")
    quantity: float = Field(..., description="Quantity of the ingredient.")
    unit: Unit = Field(..., description="Unit of measurement (e.g., piece, ml, g).")


class DishInfo(BaseModel):
    calories: int = Field(..., description="Calories per serving.")
    prep_time: int = Field(..., description="Preparation time in minutes.")
    cook_time: int = Field(..., description="Cooking time in minutes.")
    total_time: int = Field(..., description="Total time in minutes (auto-calculated).")


class Recipe(BaseModel):
    title: str = Field(..., description="Title of the recipe.")
    summary: str = Field(
        ...,
        description="Description of the dish and receipt, what it is about,"
        " what food etc. "
        "One sentence - 20 words at max.",
        max_length=70,
    )
    ingredients: list[Ingredient] = Field(..., description="List of ingredients.")
    # TODO: add pictures to the steps, make the more structured
    steps: List[str] = Field(..., description="Step-by-step instructions.")
    dish_info: DishInfo = Field(..., description="Additional information about the dish.")
    tags: List[str] = Field(..., description="Tags for categorizing the recipe.")
    photo_base64: str | None = Field(None, description="Ignore it!!!")
