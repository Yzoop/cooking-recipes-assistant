import os
from pathlib import Path

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import HttpUrl

from cooking_assistant_app.models.receipt import Recipe
from cooking_assistant_app.utils.web_utils import get_website_context

# TODO: add feature: replace ingredient / what you have or recommended
# TODO: add recommendations how to modify the receipt
# TODO: add tools what people have, like oven, air-fryer etc.


class OpenaiApiManager:
    def __init__(
        self,
        openai_api_key_name: str = "OPENAI_API_KEY",
    ):
        if (
            prompt_path := Path(__file__).parent / "openai_prompts" / "prompt_parse_url_recipe"
        ).exists():
            with open(prompt_path) as prompt_file:
                self.__prompt = prompt_file.read()
        else:
            raise FileNotFoundError(f"Prompt {prompt_path} does not exist!")
        if "{website_context}" not in self.__prompt:
            raise ValueError("Given prompt does not contain placeholder for the website url!")
        load_dotenv()
        self.__openai_client = instructor.from_openai(
            OpenAI(api_key=os.getenv(openai_api_key_name))
        )

    def get_recipe(self, website_url: HttpUrl, gpt_model: str = "gpt-4o-mini") -> Recipe:
        # Extract structured data from natural language
        processed_prompt = self.__process_prompt(website_url)
        recipe = self.__openai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_model=Recipe,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return recipe

    def __process_prompt(self, website_url: HttpUrl):
        page_content = get_website_context(website_url)
        return self.__prompt.format(website_context=page_content)
