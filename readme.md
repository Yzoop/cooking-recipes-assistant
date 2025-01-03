# Cooking Recipes Assistant - `Smachna`

## A Few Words About the Project

### What?
`Smachna` is a tool designed to help save, organize, and simplify recipes. It turns recipes from websites, TikTok, Instagram, and other sources into clean, easy-to-follow formats.

### Why?
I often face issues managing recipes:
- Websites clutter recipes with unrelated content.
- TikTok and Instagram videos require pausing or screenshotting for ingredients.
- Recipes are scattered across multiple platforms.

To solve these problems, I created `Smachna` as my personal assistant, now shared as a public API and app.

---

## Features

### Current Features
- 🥗 **Structured Recipes**  
  All recipes follow a consistent format: ingredients, steps, and dish information (calories, cooking time, etc.).
  
- 🌐 **Website and Video Parsing**  
  Parse recipes from websites, TikTok, and Instagram videos into a clean format.
  
- 🎨 **Custom Dish Images**  
  Automatically generate minimalistic, cozy illustrations for each dish using AI.

- 📚 **Recipe Library**  
  Save and organize your favorite recipes with tags and categories.

- 🔄 **Localization**  
  Full support for multiple languages with localized units, text, and app labels.

- 🖋️ **Clipboard Integration**  
  Easily paste URLs or text directly from the clipboard into the app.

- 🍽️ **Dish Classification**  
  Recipes are grouped into predefined categories (e.g., Soup, Salad, Dessert), complete with auto-generated images for most popular dishes.

- 🆕 **New Recipe Indicator**  
  A "New!" badge appears in the app when a new recipe is added.

- 🔗 **Share to App**  
  Seamlessly add recipes by sharing URLs directly from other apps like TikTok or Instagram.

### Planned Features
- 🔧 **Advanced TikTok/YouTube Parsing**  
  Improved support for parsing videos into detailed recipes.

- 📊 **Analytics and Insights**  
  Track cooking trends, ingredient popularity, and recipe usage.

- ☁️ **Cloud Sync**  
  Sync recipes across multiple devices securely.

---

## Change Log

### Recent Updates
1. **API Enhancements**  
   - Unified `/parse-recipe/` endpoint for both recipes and images.  
   - Optimized OpenAI requests for speed and cost efficiency.  

2. **Mobile App Improvements**  
   - Added "New!" badge with animation when new recipes are added.  
   - Integrated share-to-app functionality for easier recipe importing.  
   - Enhanced Recipe Detail View with better layouts, gradients, and dish info display.  

3. **Dish Classification**  
   - Auto-classify dishes into predefined categories.  
   - Updated prompt for consistent image generation.  

4. **Localization Updates**  
   - Full multi-language support with localized units and UI components.  
   - Added translations for ingredient units and other app text.  

5. **File Persistence**  
   - Recipes are now saved using `FileManager` to persist data across app sessions.  
   - Duplicate recipes are avoided using `sourceUrl` as a unique identifier.

---

## Tech Stack

- **Backend**: Python 3.12 API, OpenAI integration for LLM tasks.  
- **Mobile**: Swift for iOS-native development.  
- **Cloud**: Deployed on Heroku with best practices in cloud architecture.

---

## Roadmap

1. **TikTok Parsing**: Enhanced content extraction from TikTok videos.  
2. **Background Recipe Generation**: Support for automated scraping and recipe generation.  
3. **User Recipe Database**: Database integration for managing and syncing user recipes.  
4. **Mobile App**: Expand features like user profiles, search, and sharing.

---

## Recipe Structure

```json
{
  "title": "Spaghetti Carbonara",
  "ingredients": [
    {"name": "Spaghetti", "quantity": 200, "unit": "g"},
    {"name": "Eggs", "quantity": 2, "unit": "pcs"},
    {"name": "Parmesan cheese", "quantity": 50, "unit": "g"},
    {"name": "Bacon", "quantity": 100, "unit": "g"},
    {"name": "Black pepper", "quantity": 1, "unit": "tsp"}
  ],
  "steps": [
    "Boil spaghetti until al dente.",
    "Cook bacon in a pan until crispy.",
    "Beat eggs with grated Parmesan cheese in a bowl.",
    "Drain spaghetti and mix with the bacon.",
    "Remove from heat and mix in the egg and cheese mixture.",
    "Season with black pepper and serve immediately."
  ],
  "dish_info": {
    "calories": 450,
    "prep_time": 10,
    "cook_time": 20
  },
  "tags": ["Italian", "quick", "classic"],
  "photo_base64": "data:image/png;base64,....",
  "class": "Pasta",
  "sourceUrl": "https://example.com/spaghetti-carbonara"
}
```

## Heroku helpers
`git push heroku main` - deploy from local 

`heroku logs --tail -a cooking-assistant-api` - check the app logs

## License
This project is licensed under the Educational Community License v2.0 (ECL-2.0).  
**Note:** This code is provided strictly for educational purposes. Any commercial use is strongly discouraged.