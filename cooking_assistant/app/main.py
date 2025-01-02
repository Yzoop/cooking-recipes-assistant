import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import HttpUrl

from cooking_assistant.models.receipt import Language
from cooking_assistant.utils.prompt_manager import OpenaiApiManager

app = FastAPI()
security = HTTPBearer()
load_dotenv()

api_manager = OpenaiApiManager()

# Simulated token for demo purposes
API_TOKEN = os.environ.get("ASSISTANT_API_KEY")
print(API_TOKEN)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token")


@app.get("/", dependencies=[Depends(verify_token)])
def home():
    return {"message": "Welcome to the Recipe Parsing API!"}


@app.get("/parse-recipe/", dependencies=[Depends(verify_token)])
def parse_recipe(
    website_url: HttpUrl = Query(..., description="The URL of the recipe to parse."),
    language: Language = Query(Language.ENGLISH, description="The language of the recipe content."),
):
    try:
        recipe = api_manager.get_recipe(recipe_url=website_url, language=language)
        return recipe.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
