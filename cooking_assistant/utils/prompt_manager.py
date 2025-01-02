import base64
import io
import os
from pathlib import Path

import instructor
import requests
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
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
        self.__recipe_prompt = self.__read_prompt("prompt_parse_url_recipe")
        self.__photo_prompt = self.__read_prompt("prompt_generate_dish_photo")
        if "{website_context}" not in self.__recipe_prompt:
            raise ValueError("Given prompt does not contain placeholder for the website url!")
        load_dotenv()
        self.__openai_client = instructor.from_openai(
            OpenAI(api_key=os.getenv(openai_api_key_name))
        )
        self.tiktok_manager = TikTokManager()

    def __read_prompt(self, prompt_name: str) -> str:
        if (prompt_path := Path(__file__).parent / "openai_prompts" / prompt_name).exists():
            with open(prompt_path) as prompt_file:
                return prompt_file.read()
        else:
            raise FileNotFoundError(f"Prompt {prompt_path} does not exist!")

    def get_recipe(
        self,
        recipe_url: HttpUrl,
        gpt_model: str = "gpt-4o-mini",
        language: Language = Language.ENGLISH,
        generate_photo: bool = True,
    ) -> Recipe:
        # Extract structured data from natural language
        processed_prompt = self.__process_prompt(recipe_url, language=language)
        print("Fetching receipt!")
        recipe = self.__openai_client.chat.completions.create(
            model=gpt_model,
            response_model=Recipe,
            messages=[{"role": "user", "content": processed_prompt}],
        )
        if generate_photo:
            print("Generating photo for the receipt!")
            recipe.photo_base64 = self.generate_recipe_image(recipe_summary=recipe.summary)
        return recipe

    def generate_recipe_image(self, recipe_summary, gpt_model: str = "dall-e-3") -> str:
        """
        Generate a recipe image, convert it to Base64, and return the encoded string.

        Args:
            recipe_summary (str): Summary of the recipe to generate an image.
            gpt_model (str): The image generation model to use.

        Returns:
            str: Base64-encoded string of the generated image.
        """
        processed_prompt = self.__photo_prompt.format(summary=recipe_summary)

        # Generate image using OpenAI API
        photo_url = (
            self.__openai_client.images.generate(
                model=gpt_model,
                prompt=processed_prompt,
                # TODO: smaller size!
                size="1024x1024",
                quality="standard",
                n=1,
            )
            .data[0]
            .url
        )

        # Fetch the image from the generated URL
        response = requests.get(photo_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to download the image from {photo_url}")

        # Convert the image content to Base64
        image = Image.open(io.BytesIO(response.content))
        resized_image = image.resize((512, 512))

        # Convert the resized image to Base64
        buffer = io.BytesIO()
        resized_image.save(buffer, format="PNG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return image_base64

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
