import os
from uuid import UUID

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import HttpUrl

from cooking_assistant.models.recipe_models import Language
from cooking_assistant.recipe.recipe_manager import RecipeManager

app = FastAPI()
security = HTTPBearer()
load_dotenv()

recipe_manager = RecipeManager()

# Simulated token for demo purposes
API_TOKEN = os.environ.get("ASSISTANT_API_KEY")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token")


@app.get("/", dependencies=[Depends(verify_token)])
def home():
    return {"message": "Welcome to the Recipe Parsing API!"}


@app.put("/send-recipe/", dependencies=[Depends(verify_token)])
async def send_recipe(
    user_id: str,
    recipe_url: HttpUrl,
    language: Language = Query(Language.ENGLISH.value, description="Language of the recipe"),
):
    """
    Add a new recipe for a user. If the recipe already exists, returns the existing recipe.
    """
    try:
        # Attempt to create or retrieve the recipe
        recipe_id = await recipe_manager.create_recipe(
            language=language, user_id=user_id, recipe_url=recipe_url
        )
        # If the recipe is newly created, process it asynchronously
        # Respond with only the recipe ID

        return {"id": recipe_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add recipe: {e}")


@app.get("/get-recipe/", dependencies=[Depends(verify_token)])
async def get_recipe(
    user_id: str,
    recipe_id: UUID,
    language: Language = Query(Language.ENGLISH.value, description="Language of the recipe"),
):
    """
    Retrieve a specific recipe by user ID and recipe ID.
    """
    try:
        recipe = recipe_manager.get_recipe(language=language, user_id=user_id, recipe_id=recipe_id)
        if recipe:
            return recipe.model_dump()
        else:
            raise HTTPException(status_code=404, detail="Recipe not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve recipe: {e}")
