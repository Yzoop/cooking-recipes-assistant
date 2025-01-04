import asyncio

from pydantic import HttpUrl

from cooking_assistant.models.recipe_models import Language
from cooking_assistant.recipe.recipe_manager import RecipeManager

if __name__ == "__main__":
    recipe_manager = RecipeManager()
    res = asyncio.run(
        recipe_manager.create_recipe(
            language=Language.UKRAINIAN,
            user_id="user_a",
            recipe_url=HttpUrl("https://vm.tiktok.com/ZMkAKXcth/"),
        )
    )
    print(res)
