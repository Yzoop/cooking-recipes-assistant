from fastapi import FastAPI, HTTPException
from pydantic import HttpUrl

from cooking_assistant_app.utils.prompt_manager import OpenaiApiManager

app = FastAPI()

# Initialize OpenAI API Manager
api_manager = OpenaiApiManager()


@app.get("/")
def home():
    return {"message": "Welcome to the Recipe Parsing API!"}


@app.post("/parse-recipe/")
def parse_recipe(website_url: HttpUrl):
    try:
        recipe = api_manager.get_recipe(website_url=website_url)
        return recipe.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
