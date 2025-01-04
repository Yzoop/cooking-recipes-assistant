from enum import StrEnum
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class DbStatus(StrEnum):
    READY = "ready"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"


class Unit(StrEnum):
    PIECES = "pieces"
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


class RecipeLanguageSensitiveInfo(BaseModel):
    title: str | None = None
    summary: str | None = None
    ingredients: list[Ingredient] | None = None
    steps: List[str] | None = None
    dish_info: DishInfo | None = None
    tags: List[str] | None = None


class RecipeInfo(RecipeLanguageSensitiveInfo):
    # TODO: add pictures to the steps, make the more structured
    photo_base64: str | None = None


class _PhotoBase64(BaseModel):
    photo_base64: str | None = None


class Recipe(RecipeInfo):
    id: UUID
    status: DbStatus
    source_url: HttpUrl


class _Title(BaseModel):
    title: str = Field(..., description="Title of the recipe.")


class _Summary(BaseModel):
    summary: str = Field(
        ...,
        description="A concise, vivid description of the dish,"
        "focusing on its key ingredients, presentation, and cooking style. "
        "Include sensory or visual cues to make it vivid but keep it within 7-12 words "
        "(80 characters maximum!!).",
        max_length=80,
    )


class _DishInfo(BaseModel):
    dish_info: DishInfo


class _Ingredients(BaseModel):
    ingredients: list[Ingredient] = Field(..., description="List of ingredients")


class _Steps(BaseModel):
    steps: List[str] = Field(
        ..., description="Precise, step-by-step instructions on how to make the dish."
    )


class _Tags(BaseModel):
    tags: List[str] = Field(..., description="Tags for categorizing the recipe.")
