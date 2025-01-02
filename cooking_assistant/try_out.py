from pydantic import HttpUrl

from cooking_assistant.models.receipt import Language
from cooking_assistant.utils.prompt_manager import OpenaiApiManager

# from cooking_assistant.utils.web_utils import TikTokManager

if __name__ == "__main__":
    prompt_manager = OpenaiApiManager()
    print(
        prompt_manager.get_recipe(
            recipe_url=HttpUrl("https://vm.tiktok.com/ZMkAKXcth/"), language=Language.UKRAINIAN
        )
    )
    # tt_manager = TikTokManager()
    # tt_manager.get_tiktok_captions(
    #     tt_video_url=HttpUrl(
    #         "https://www.tiktok.com/@martellifoods/video/7124401218184596742"
    #         "?is_from_webapp=1&sender_device=pc&web_id=7383700479904171552"
    #     )
    # )
