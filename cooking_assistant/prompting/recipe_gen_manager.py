import base64
import os
from typing import AsyncGenerator

import instructor
import requests
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel, HttpUrl

from cooking_assistant.models.recipe_models import (
    DishInfo,
    Language,
    _DishInfo,
    _Ingredients,
    _PhotoBase64,
    _Steps,
    _Summary,
    _Title,
)
from cooking_assistant.prompting.image_generator import ImageGenerator
from cooking_assistant.prompting.prompt_utils import read_prompt
from cooking_assistant.web.tiktok import TikTokManager
from cooking_assistant.web.web_utils import UrlType, get_website_context, type_of_url

# TODO: add feature: replace ingredient / what you have or recommended
# TODO: add recommendations how to modify the recipe
# TODO: add tools what people have, like oven, air-fryer etc.
# TODO: add counter on how many people the recipe is,
#  adjust (add formula) the recipe to be multiplied for several people.


class RecipeGenerator:
    def __init__(
        self,
        openai_api_key_name: str = "OPENAI_API_KEY",
    ):
        self.__recipe_prompt = read_prompt("prompt_parse_url_recipe")
        self.__photo_prompt = read_prompt("prompt_generate_dish_photo")
        self.__translate_prompt = read_prompt("prompt_translate_summary")
        if "{website_context}" not in self.__recipe_prompt:
            raise ValueError("Given prompt does not contain placeholder for the website url!")
        load_dotenv()
        self.__openai_client = instructor.patch(AsyncOpenAI(api_key=os.getenv(openai_api_key_name)))
        self.tiktok_manager = TikTokManager()
        self.img_gen_manager = ImageGenerator()

    async def generate_recipe_fields(
        self, language: Language, source_url: HttpUrl
    ) -> AsyncGenerator[tuple[str, BaseModel], None]:
        """
        Generate recipe fields incrementally.

        :param source_url: The URL of the recipe to process.
        :yield: Tuples of field name and its generated value.
        """
        processed_prompt = self.__process_prompt(recipe_url=source_url, language=language)
        print("Started extracting recipe parts...")

        field_generators = {
            "title": self.fetch_title(processed_prompt, "gpt-3.5-turbo"),
            "summary": self.fetch_summary(processed_prompt, "gpt-4o-mini"),
            "ingredients": self.fetch_ingredients(processed_prompt, "gpt-4o"),
            "dish_info": self.fetch_dish_info(processed_prompt, "gpt-4o-mini"),
            "steps": self.fetch_steps(processed_prompt, "gpt-4o-mini"),
        }

        for field_name, field_generation_call in field_generators.items():
            field_value = await field_generation_call
            # If the summary is generated, trigger the image generation
            if field_name == "summary" and field_value is not None:
                english_summary = await self.__translate(
                    dish_summary=field_value.summary, gpt_model="gpt-4o-mini"
                )
                img_bas64 = await self.img_gen_manager.generate_image(
                    english_summary.summary,
                    return_type="base64_str",
                )
                yield "photo_base64", _PhotoBase64(photo_base64=img_bas64)
            yield field_name, field_value

    def __translate(self, *, dish_summary: str, gpt_model: str):
        # for iamge generation logic, translates to english,
        # as current image generator only supports english prompts
        processed_prompt = self.__translate_prompt.format(
            text_to_translate=dish_summary, language=Language.ENGLISH.name
        )
        response = self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Summary,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    def __process_prompt(self, recipe_url: HttpUrl, language: Language):
        """Processes the URL to create a prompt for OpenAI API."""
        url_type = type_of_url(recipe_url)
        if url_type == UrlType.tiktok_url:
            content = self.tiktok_manager.get_tiktok_captions(tt_video_url=recipe_url)
        elif url_type == UrlType.web_page_url:
            content = get_website_context(recipe_url)
        else:
            raise NotImplementedError(f"The URL type for {recipe_url} is not implemented.")

        return self.__recipe_prompt.format(website_context=content, language=language.name)

    async def fetch_title(self, processed_prompt: str, gpt_model: str) -> _Title:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Title,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_summary(self, processed_prompt: str, gpt_model: str) -> _Summary:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Summary,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_ingredients(self, processed_prompt: str, gpt_model: str) -> _Ingredients:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Ingredients,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_steps(self, processed_prompt: str, gpt_model: str) -> _Steps:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Steps,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_dish_info(self, processed_prompt: str, gpt_model: str) -> DishInfo:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_DishInfo,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_recipe_image(self, recipe_summary: str) -> str:
        processed_prompt = self.__photo_prompt.format(summary=recipe_summary)
        response = await self.__openai_client.images.generate(
            model="dall-e-2",
            prompt=processed_prompt,
            size="256x256",
            quality="standard",
            n=1,
        )
        return base64.b64encode(requests.get(response.data[0].url).content).decode("utf-8")
