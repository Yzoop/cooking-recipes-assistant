import base64
import os

import instructor

# Set up OpenAI API key
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Dish classes and their descriptions
dish_classes = {
    "SOUP": "A bowl of creamy tomato soup with a sprinkle of fresh herbs.",
    "SALAD": "A fresh green salad with lettuce, cucumbers, and a drizzle of olive oil.",
    "PASTA": "A plate of spaghetti with marinara sauce and fresh basil leaves.",
    "PIZZA": "A slice of margherita pizza with melted cheese and a basil garnish.",
    "CURRY": "A bowl of chicken curry with a side of steamed rice.",
    "BREAD": "A freshly baked loaf of sourdough bread on a wooden board.",
    "BURGER": "A classic cheeseburger with lettuce, tomato, and a sesame seed bun.",
    "SANDWICH": "A club sandwich layered with turkey, lettuce, and tomatoes.",
    "DESSERT": "A slice of chocolate cake with a dollop of whipped cream.",
    "DRINK": "A refreshing glass of lemonade with ice cubes and a lemon wedge.",
    "MEAT": "A grilled steak served with roasted potatoes and a sprig of rosemary.",
    "FISH": "A grilled salmon fillet with a lemon wedge and steamed asparagus.",
    "RICE": "A bowl of fried rice with colorful vegetables and soy sauce.",
    "NOODLES": "A plate of stir-fried noodles with shrimp and scallions.",
    "STEW": "A hearty beef stew with chunks of carrots and potatoes.",
    "SNACK": "A small bowl of crunchy nachos with cheese dip.",
    "EGG": "A fluffy omelet filled with cheese and mushrooms.",
    "CHEESE": "A gooey bowl of mac and cheese topped with bread crumbs.",
    "VEGAN": "A colorful Buddha bowl with quinoa, avocado, and fresh vegetables.",
    "FRUIT": "A bowl of mixed fruit with strawberries, blueberries, and a mint garnish.",
}

# Prompt template for DALL-E
prompt_template = (
    "Create a cozy, minimalistic digital illustration of a {summary} plated in the center, "
    "inspired by the key ingredients typical for the {dish_class} category. "
    "The illustration should evoke a warm and inviting feeling, "
    "with soft, muted tones matching the app’s color palette: "
    "a warm cream background (#fff8df), soft yellow highlights (#f2d776), and light beige accents. "
    "Avoid clutter, ensure the dish is clean, simple, "
    "and uniformly styled with a drawn look rather than photorealistic."
)

# Output directory
output_dir = "dish_images"
os.makedirs(output_dir, exist_ok=True)

load_dotenv()
openai_client = instructor.patch(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# Generate and save images
for dish_class, summary in dish_classes.items():
    prompt = prompt_template.format(summary=summary, dish_class=dish_class)

    try:
        # Generate image
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            # TODO: smaller size!
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        # Fetch image and encode as base64
        image_data = requests.get(image_url).content
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        # Save to file
        file_path = os.path.join(output_dir, f"{dish_class.lower()}_image.txt")
        with open(file_path, "w") as file:
            file.write(image_base64)

        print(f"Generated and saved image for {dish_class}.")

    except Exception as e:
        print(f"Failed to generate image for {dish_class}: {e}")
