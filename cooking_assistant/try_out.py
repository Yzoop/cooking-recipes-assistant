from pydantic import HttpUrl

from cooking_assistant.utils.web_utils import TikTokManager

if __name__ == "__main__":
    # prompt_manager = OpenaiApiManager()
    # print(
    #     prompt_manager.get_recipe(
    #         website_url=HttpUrl("https://www.indianhealthyrecipes.com/pizza-recipe-make-pizza/")
    #     )
    # )
    tt_manager = TikTokManager()
    tt_manager.get_tiktok_captions(
        tt_video_url=HttpUrl(
            "https://www.tiktok.com/@martellifoods/video/7124401218184596742"
            "?is_from_webapp=1&sender_device=pc&web_id=7383700479904171552"
        )
    )
