import asyncio

from cooking_assistant.prompting.image_generator import ImageGenerator

if __name__ == "__main__":
    # recipe_manager = RecipeManager()
    # res = asyncio.run(
    #     recipe_manager.create_recipe(
    #         language=Language.UKRAINIAN,
    #         user_id="user_a",
    #         recipe_url=HttpUrl("https://vm.tiktok.com/ZMkAKXcth/"),
    #     )
    # )
    # print(res)

    img_gen = ImageGenerator()
    res = asyncio.run(img_gen.generate_image("tasty fish", return_type="base64_str"))
    print(res)
