from pathlib import Path

from utils.prompt_manager import OpenaiApiManager

if __name__ == "__main__":
    prompt_manager = OpenaiApiManager(prompt_path=Path("./openai_prompts/prompt_parse_url_recipe"))
    print(
        prompt_manager.get_recipe(
            website_url="https://www.indianhealthyrecipes.com/pizza-recipe-make-pizza/"
        )
    )
