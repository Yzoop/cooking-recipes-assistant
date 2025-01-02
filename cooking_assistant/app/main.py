import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import HttpUrl

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
def parse_recipe(website_url: HttpUrl):
    try:
        recipe = api_manager.get_recipe(recipe_url=website_url)
        return recipe.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
