import asyncio
import datetime
from uuid import UUID

from pydantic import HttpUrl

from cooking_assistant.database.db_manager import RecipeDbManager
from cooking_assistant.models.recipe_models import DbStatus, Language, Recipe
from cooking_assistant.prompting.recipe_gen_manager import RecipeGenerator
from cooking_assistant.recipe.utils import generate_recipe_id


class RecipeManager:
    def __init__(self):
        self.db_manager = RecipeDbManager()
        self.recipe_generator = RecipeGenerator()

    def get_recipe(
        self,
        language: Language,
        user_id: str,
        recipe_id: UUID,
    ) -> Recipe | None:
        # Check if the recipe already exists
        existing_recipe = self.db_manager.get_recipe(language, user_id, recipe_id)
        if existing_recipe:
            return existing_recipe
        else:
            return None

    async def create_recipe(
        self, language: Language, user_id: str, recipe_url: HttpUrl, check_exists: bool = True
    ) -> UUID:
        # Check if the recipe already exists
        recipe_id = generate_recipe_id(recipe_url)
        if check_exists and (
            recipe := self.get_recipe(language=language, user_id=user_id, recipe_id=recipe_id)
        ):
            # recreate logic
            if recipe.status != DbStatus.FAILED:
                return recipe_id
            else:
                self.db_manager.delete_recipe(user_id=user_id, recipe_id=recipe.id)

        # Create a new recipe
        new_recipe = Recipe(
            id=recipe_id,
            source_url=recipe_url,
            status=DbStatus.IN_PROGRESS,
            date_created_at=datetime.datetime.today().date(),
        )
        self.db_manager.add_recipe(language, user_id, new_recipe)

        # Process the recipe asynchronously
        asyncio.create_task(
            self._process_recipe(language=language, user_id=user_id, recipe=new_recipe)
        )

        return recipe_id

    async def _process_recipe(self, *, language: Language, user_id: str, recipe: Recipe):
        try:
            # Start the recipe generation process
            async for field_name, field_value in self.recipe_generator.generate_recipe_fields(
                language=language, source_url=recipe.source_url
            ):
                if field_value is not None:
                    recipe = Recipe(**(recipe.dict() | field_value.dict()))
                    recipe.status = DbStatus.IN_PROGRESS
                    self.db_manager.update_recipe(language, user_id, recipe)
                    print(f"Updated {field_name} for recipe {recipe.id}: {field_value}")
            recipe.status = DbStatus.READY
            self.db_manager.update_recipe(language=language, user_id=user_id, recipe=recipe)
            print(f"Recipe {recipe.id} processing complete.")
        except Exception as e:
            print(f"Error processing recipe {recipe.id}: {e}")
            # Mark the recipe as failed in case of any error
            recipe.status = DbStatus.FAILED
            self.db_manager.update_recipe(language, user_id, recipe)

    def get_recipe_ids(self, user_id: str) -> list[UUID]:
        recipe_ids = self.db_manager.get_recipe_ids(user_id=user_id)
        return recipe_ids
