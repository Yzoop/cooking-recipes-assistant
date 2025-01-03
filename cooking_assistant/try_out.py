import asyncio
import time

from pydantic import HttpUrl

from cooking_assistant.utils.prompt_manager import OpenaiApiManager

if __name__ == "__main__":
    # summary = "Смачний лосось в аерогрилі за простим і швидким рецептом."
    # prompt_manager = OpenaiApiManager()
    # taken_times = {"dall-e-2": [], "dall-e-3": []}
    # for model in taken_times.keys():
    #     print(os.path.exists(f"generated_photos/{model}"))
    #     for i in range(5):
    #         start_time = time.time()
    #         base_64 = prompt_manager.generate_recipe_image(
    #             recipe_summary=summary, gpt_model=model, size="256x256"
    #         )
    #         taken_times[model].append(time.time() - start_time)
    #
    #         img = Image.open(io.BytesIO(base64.decodebytes(bytes(base_64, "utf-8"))))
    #         img.save(f"generated_photos/{model}/{i}_dish.png")
    # print(taken_times)

    manager = OpenaiApiManager()
    for _ in range(5):
        start = time.time()
        receipt = asyncio.run(
            manager.get_recipe(
                recipe_url=HttpUrl(
                    "https://www.tiktok.com/@tastelessbaker/video/7229542242506116353"
                ),
                generate_image=True,
                gpt_model="gpt-4o-mini",
            )
        )
        receipt
        print(receipt)
        print(time.time() - start)
