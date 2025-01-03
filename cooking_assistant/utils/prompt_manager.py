import base64
import os
from pathlib import Path

import aiohttp
import instructor
import requests
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import HttpUrl

from cooking_assistant.models.receipt import (
    DishClass,
    DishInfo,
    Language,
    Recipe,
    _DishClassPrediction,
    _Ingredients,
    _Steps,
    _Summary,
    _Tags,
    _Title,
)
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
        self.__recipe_prompt = self.__read_prompt("prompt_parse_url_recipe")
        self.__photo_prompt = self.__read_prompt("prompt_generate_dish_photo")
        self.__dish_images = self.__get_dish_images()
        if "{website_context}" not in self.__recipe_prompt:
            raise ValueError("Given prompt does not contain placeholder for the website url!")
        load_dotenv()
        self.__openai_client = instructor.patch(AsyncOpenAI(api_key=os.getenv(openai_api_key_name)))
        self.tiktok_manager = TikTokManager()

    def __read_prompt(self, prompt_name: str) -> str:
        if (prompt_path := Path(__file__).parent / "openai_prompts" / prompt_name).exists():
            with open(prompt_path) as prompt_file:
                return prompt_file.read()
        else:
            raise FileNotFoundError(f"Prompt {prompt_path} does not exist!")

    def __get_dish_images(self) -> dict[str, str]:
        """
        Load all Base64-encoded images from the directory into memory.
        """
        dish_class_images: dict[str, str] = {}
        for dish_class in DishClass:
            filename = f"{dish_class.name.lower()}_image.txt"
            filepath = os.path.join(Path(__file__).parent / "dish_images", filename)
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    dish_class_images[dish_class.name] = file.read()
            else:
                print(f"Warning: Missing image for class {dish_class.name}")
        return dish_class_images

    async def get_recipe(
        self,
        recipe_url: HttpUrl,
        gpt_model: str = "gpt-4o-mini",
        language: Language = Language.ENGLISH,
        generate_image: bool = False,
    ) -> Recipe:
        # Preprocess the prompt once
        processed_prompt = self.__process_prompt(recipe_url, language)
        print("Started extracting recipe parts...")
        title = self.fetch_title(processed_prompt, gpt_model="gpt-3.5-turbo")
        summary = self.fetch_summary(processed_prompt, gpt_model=gpt_model)
        ingredients = self.fetch_ingredients(processed_prompt, gpt_model=gpt_model)
        steps = self.fetch_steps(processed_prompt, gpt_model=gpt_model)
        # tags = self.fetch_tags(processed_prompt, gpt_model=gpt_model)
        dish_info = self.fetch_dish_info(processed_prompt, gpt_model=gpt_model)

        # Generate class for the receipt to get pre-generated image
        dish_class = self.fetch_dish_class(processed_prompt, gpt_model=gpt_model)

        # Create the Recipe object once all data is available
        recipe = Recipe(
            title=(await title).title,
            source_url=recipe_url,
            summary=(await summary).summary,
            ingredients=(await ingredients).ingredients,
            steps=(await steps).steps,
            tags=[],  # (await tags).tags,
            dish_info=await dish_info,
            photo_base64=self.__dish_images[(await dish_class).dish_class.name],
        )

        return recipe

    def __process_image(self, openai_image_response) -> str:
        return base64.b64encode(requests.get(openai_image_response.data[0].url).content).decode(
            "utf-8"
        )

    async def fetch_title(self, processed_prompt: str, gpt_model: str) -> object:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Title,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_summary(self, processed_prompt: str, gpt_model: str) -> object:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Summary,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_steps(self, processed_prompt: str, gpt_model: str) -> object:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Steps,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_dish_info(self, processed_prompt: str, gpt_model: str) -> object:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=DishInfo,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_dish_class(self, processed_prompt: str, gpt_model: str) -> object:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_DishClassPrediction,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_ingredients(self, processed_prompt: str, gpt_model: str) -> object:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Ingredients,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        return response

    async def fetch_tags(self, processed_prompt: str, gpt_model: str) -> object:
        response = await self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=_Tags,
            messages=[{"role": "user", "content": processed_prompt}],
            max_retries=3,
        )
        return response

    async def fetch_recipe_image(self, recipe_summary: str) -> str:
        processed_prompt = self.__photo_prompt.format(summary=recipe_summary)
        # Generate image using OpenAI API

        return await self.__openai_client.images.generate(
            model="dall-e-2",
            prompt=processed_prompt,
            # TODO: smaller size!
            size="256x256",
            quality="standard",
            n=1,
        )

    async def download_image(self, image_url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    return base64.b64encode(image_data).decode("utf-8")
        return ""

    def __process_prompt(self, recipe_url: HttpUrl, language: Language):
        if (url_type := type_of_url(recipe_url)) == UrlType.tiktok_url:
            content = self.tiktok_manager.get_tiktok_captions(tt_video_url=recipe_url)
        elif url_type == UrlType.web_page_url:
            content = get_website_context(recipe_url)
        else:
            raise NotImplementedError(f"The URL type for {recipe_url} is not implemented.")
        # TODO: add content filter, i.e. vulnurable,
        #  not related to cooking, not enough information etc.
        return self.__recipe_prompt.format(website_context=content, language=language.name)
