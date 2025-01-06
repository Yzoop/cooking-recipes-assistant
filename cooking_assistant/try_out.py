# import asyncio
# from uuid import UUID
#
# from pydantic import HttpUrl
#
# from cooking_assistant.database.db_manager import RecipeDbManager
# from cooking_assistant.models.recipe_models import Language
# from cooking_assistant.prompting.image_generator import ImageGenerator
# from cooking_assistant.recipe.recipe_manager import RecipeManager
#
# if __name__ == "__main__":
#     recipe_manager = RecipeManager()
#     res = asyncio.run(
#         recipe_manager.create_recipe(
#             language=Language.ENGLISH,
#             user_id="3Gl9L5VDwIMZ4OZBLLnlH5JLnI12",
#             recipe_url=HttpUrl("https://www.tiktok.com/@boredoflunch/video/7330668395534241057?lang=en"),
#         )
#     )
#     print(res)
#     # db_manager = RecipeDbManager()
#     # print(db_manager.get_recipe_ids(user_id="user_a"))
#     # img_gen = ImageGenerator()
#     # res = asyncio.run(img_gen.generate_image("tasty fish", return_type="base64_str"))
#     # print(res)
