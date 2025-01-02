import os
from pathlib import Path

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import HttpUrl

from cooking_assistant.models.receipt import Language, Recipe
from cooking_assistant.utils.web_utils import (
    TikTokManager,
    UrlType,
    get_website_context,
    type_of_url,
)

# TODO: add feature: replace ingredient / what you have or recommended
# TODO: add recommendations how to modify the receipt
# TODO: add tools what people have, like oven, air-fryer etc.
# TODO: add counter on how many people the receipt is,
#  adjust (add formula) the recipe to be multiplied for several people.


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
        self.tiktok_manager = TikTokManager()

    def get_recipe(
        self,
        recipe_url: HttpUrl,
        gpt_model: str = "gpt-4o-mini",
        language: Language = Language.ENGLISH,
    ) -> Recipe:
        # Extract structured data from natural language
        processed_prompt = self.__process_prompt(recipe_url, language=language)
        recipe = self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=Recipe,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return recipe

    def __process_prompt(self, recipe_url: HttpUrl, language: Language):
        if (url_type := type_of_url(recipe_url)) == UrlType.tiktok_url:
            content = self.tiktok_manager.get_tiktok_captions(tt_video_url=recipe_url)
        elif url_type == UrlType.web_page_url:
            content = get_website_context(recipe_url)
        else:
            raise NotImplementedError(f"The URL type for {recipe_url} is not implemented.")
        # TODO: add content filter, i.e. vulnurable,
        #  not related to cooking, not enough information etc.
        return self.__prompt.format(website_context=content, language=language.name)
