import base64
import io
import os

import requests
from dotenv import load_dotenv
from PIL import Image

from cooking_assistant.prompting.prompt_utils import read_prompt


class ImageGenerator:
    def __init__(self, getimg_api_key_name: str = "GETIMG_API_AI_KEY"):
        load_dotenv()
        self.__headers = {
            "Authorization": f"Bearer {os.environ.get(getimg_api_key_name)}",
            "Content-Type": "application/json",
        }
        self.__default_prompt = read_prompt(prompt_name="prompt_generate_dish_photo")
        self.__default_getimg_endpoint = "https://api.getimg.ai/v1/flux-schnell/text-to-image"

    async def generate_image(self, english_dish_description: str, return_type: str):
        img_base64 = await self.__request_getimg(english_dish_description)
        # Convert to an image
        if return_type == "base64_str":
            return base64.b64encode(img_base64).decode("utf-8")
        elif return_type == "image":
            return Image.open(io.BytesIO(img_base64))
        else:
            raise NotImplementedError(
                f"{return_type} not supported as return type for image generation!"
            )

    async def __request_getimg(
        self, dish_description: str, width: int = 512, height: int = 512, quality_steps: int = 3
    ) -> bytes:
        processed_prompt = self.__default_prompt.format(summary=dish_description)

        # Define the JSON data for generating the image
        generation_data = {
            "prompt": processed_prompt,
            # Your prompt for generating the image
            "output_format": "png",  # Specify JPEG format
            "width": width,  # Your desired width
            "height": height,  # Your desired height
            "steps": quality_steps,  # Mean - quality
            "response_format": "b64",
        }
        # Make a POST request to generate the image
        response_generation = requests.post(
            self.__default_getimg_endpoint, headers=self.__headers, json=generation_data
        )
        # TODO: add error handling
        # Check if the generation request was successful (status code 200)
        response_generation.raise_for_status()
        # Parse the response JSON for the generated image
        generated_data = response_generation.json()
        # Decode the base64 image string
        generated_image_data = base64.b64decode(generated_data["image"])
        return generated_image_data
