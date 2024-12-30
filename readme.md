# Cooking recipes assistant -
**RecipeEase** is a cozy and intuitive mobile recipe app designed to simplify cooking. It allows users to search, save, and transform recipes into a clean, structured format. Powered by modern technologies like Python, Swift, and the latest LLM APIs, RecipeEase delivers a seamless experience for food enthusiasts.  

## Features  
- 🥗 **Structured Recipes**: All recipes have a consistent format with ingredients, steps, and dish information (calories, cooking time, etc.).  
- 🌐 **Website Parsing**: Share a recipe link, and the app converts it into a clean, usable recipe.  
- 🎥 **Future Vision**: Support for parsing TikTok, YouTube, and Instagram videos into step-by-step recipes.  
- 📚 **User Recipe Library**: Save and organize your favorite recipes with tags and categories.  

## Tech Stack  
- **Backend**: Python 3.12 API.  
- **Mobile**: Swift for iOS-native development with smooth animations and lightweight performance.  
- **Cloud**: Best practices in modern cloud architecture (to be shared as development progresses).  

## Roadmap  
- ✅ Design recipe structure.  
- ✅ MVP: Parse websites into structured recipes.  
- ⬜ Add TikTok/Video parsing.  
- ⬜ Build user recipe database.  
- ⬜ Develop a cozy iOS app with SwiftUI.  

## Contribute  
RecipeEase is an open-source project! Contributions, feature suggestions, and feedback are welcome.  

## Recipe structure
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
  "tags": ["Italian", "quick", "classic"]
}
```

## License
This project is licensed under the Educational Community License v2.0 (ECL-2.0).  
**Note:** This code is provided strictly for educational purposes. Any commercial use is strongly discouraged.