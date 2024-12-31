from pydantic import HttpUrl

from cooking_assistant.utils.prompt_manager import OpenaiApiManager

if __name__ == "__main__":
    prompt_manager = OpenaiApiManager()
    print(
        prompt_manager.get_recipe(
            website_url=HttpUrl("https://www.indianhealthyrecipes.com/pizza-recipe-make-pizza/")
        )
    )
