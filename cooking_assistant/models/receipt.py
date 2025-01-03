from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field, HttpUrl


class Unit(StrEnum):
    PIECE = "piece"
    MILILITER = "ml"
    LITER = "l"
    MILIGRAMM = "mg"
    GRAMM = "g"
    KILOGRAMM = "kg"
    TEASPOON = "teaspoon"
    TABLESPOON = "tablespoon"
    CLOVE = "clove"


class Language(StrEnum):
    UKRAINIAN = "uk"
    ENGLISH = "en"
    BELARUSIAN = "by"


class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient.")
    quantity: float = Field(..., description="Quantity of the ingredient.")
    unit: Unit = Field(
        ...,
        description="Unit of measurement (e.g., piece, ml, g). "
        "You must only use the available ones! No cloves, etc."
        "It is a python StrEnum, so PLEASE ONLY GIVE unit with value from Unit!!",
    )


class DishInfo(BaseModel):
    calories: int = Field(..., description="Calories per serving.")
    cook_time: int = Field(..., description="All the cooking time in minutes.")


class Recipe(BaseModel):
    title: str = Field(..., description="Title of the recipe.")
    source_url: HttpUrl = Field(..., description="Source url")
    summary: str = Field(
        ...,
        description="Description of the dish and receipt, what it is about,"
        " what food etc. "
        "One sentence 10-15 words at max.",
        max_length=100,
    )
    ingredients: list[Ingredient] = Field(..., description="List of ingredients.")
    # TODO: add pictures to the steps, make the more structured
    steps: List[str] = Field(
        ..., description="Precise, step-by-step instructions on how to make the dish."
    )
    dish_info: DishInfo = Field(..., description="Additional information about the dish.")
    tags: List[str] = Field(..., description="Tags for categorizing the recipe.")
    photo_base64: str | None = Field(None, description="Ignore it!!!")


class _Title(BaseModel):
    title: str = Field(..., description="Title of the recipe.")


class _Summary(BaseModel):
    summary: str = Field(
        ...,
        description="A concise, vivid description of the dish,"
        "focusing on its key ingredients, presentation, and cooking style. "
        "Include sensory or visual cues to make it vivid but keep it within 15-20 words "
        "(120 characters max).",
        max_length=120,
    )


class _Ingredients(BaseModel):
    ingredients: list[Ingredient] = Field(..., description="List of ingredients")


class _Steps(BaseModel):
    steps: List[str] = Field(
        ..., description="Precise, step-by-step instructions on how to make the dish."
    )


class _Tags(BaseModel):
    tags: List[str] = Field(..., description="Tags for categorizing the recipe.")
