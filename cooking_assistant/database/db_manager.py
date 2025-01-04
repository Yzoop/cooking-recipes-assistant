import json
import os.path
from pathlib import Path
from uuid import UUID

import firebase_admin
from firebase_admin import credentials, firestore

from cooking_assistant.models.recipe_models import Language, Recipe


class RecipeDbManager:
    def __init__(self):
        # Initialize Firestore
        cred = credentials.Certificate(self.__get_credentials_path())
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()

    def __get_credentials_path(self):
        path = Path(__file__).parent / "firebase-credentials.json"
        if path.exists():
            return path
        else:
            credentials = dict(
                type=os.environ["firebase_type"],
                project_id=os.environ["firebase_project_id"],
                private_key_id=os.environ["firebase_private_key_id"],
                private_key=os.environ["firebase_private_key"].replace("__NEW_LINE__", "\n"),
                client_email=os.environ["firebase_client_email"],
                client_id=os.environ["firebase_client_id"],
                auth_uri=os.environ["firebase_auth_uri"],
                token_uri=os.environ["firebase_token_uri"],
                auth_provider_x509_cert_url=os.environ["firebase_auth_provider_x509_cert_url"],
                client_x509_cert_url=os.environ["firebase_client_x509_cert_url"],
                universe_domain=os.environ["firebase_universe_domain"],
            )
            with open(path, "w+", encoding="utf-8") as credentials_json:
                json.dump(credentials, credentials_json, indent=4, ensure_ascii=False)

    def get_recipe(self, language: Language, user_id: str, recipe_id: UUID) -> Recipe | None:
        """
        Retrieve a recipe by its ID for a specific user and language.
        """
        doc_ref = (
            self.client.collection("users")
            .document(user_id)
            .collection("recipes")
            .document(str(recipe_id))
            .collection("languages")
            .document(language.name)  # Access the document under the language key
        )
        doc = doc_ref.get()
        if doc.exists:
            return Recipe(**doc.to_dict())
        else:
            return None

    def add_recipe(self, language: Language, user_id: str, recipe: Recipe):
        """
        Add a new recipe for a specific user and language.
        """
        doc_ref = (
            self.client.collection("users")
            .document(user_id)
            .collection("recipes")
            .document(str(recipe.id))
            .collection("languages")
            .document(language.name)
        )
        doc_ref.set(recipe.model_dump(mode="json"))

    def update_recipe(self, language: Language, user_id: str, recipe: Recipe):
        """
        Update an existing recipe for a specific user and language.
        """
        doc_ref = (
            self.client.collection("users")
            .document(user_id)
            .collection("recipes")
            .document(str(recipe.id))
            .collection("languages")
            .document(language.name)
        )
        doc_ref.update(recipe.model_dump(mode="json", exclude_unset=True))

    def delete_recipe(self, user_id: str, recipe_id: UUID) -> None:
        """
        Delete a recipe by its ID for a specific user.
        """
        recipes_ref = self.client.collection("users").document(user_id).collection("recipes")

        # Query to find the recipe by ID
        query = recipes_ref.where("id", "==", str(recipe_id)).limit(1).get()

        if not query:
            print(f"No recipe found with ID: {recipe_id}")
            return

        # Extract the document and delete it
        for doc in query:
            recipes_ref.document(doc.id).delete()
            print(f"Recipe with ID {recipe_id} has been deleted.")
