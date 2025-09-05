"""
Recipe recommendation system for expiring food items
"""
import random

class RecipeRecommender:
    def __init__(self):
        self.recipe_database = self._load_recipe_database()
    
    def _load_recipe_database(self):
        """Load recipe database with ingredients and instructions"""
        # In a real implementation, this would be loaded from a database or file
        recipes = {
            'scrambled_eggs': {
                'name': 'Scrambled Eggs',
                'ingredients': ['egg', 'milk'],
                'instructions': '1. Crack eggs into a bowl\n2. Add milk and whisk\n3. Cook in a pan over medium heat\n4. Stir continuously until set',
                'preparation_time': 10
            },
            'banana_bread': {
                'name': 'Banana Bread',
                'ingredients': ['banana', 'bread', 'egg'],
                'instructions': '1. Mash bananas\n2. Mix with eggs\n3. Add bread cubes\n4. Bake at 180°C for 20 minutes',
                'preparation_time': 30
            },
            'tomato_salad': {
                'name': 'Tomato Salad',
                'ingredients': ['tomato', 'lettuce'],
                'instructions': '1. Chop tomatoes and lettuce\n2. Mix together\n3. Add dressing to taste',
                'preparation_time': 10
            },
            'fruit_smoothie': {
                'name': 'Fruit Smoothie',
                'ingredients': ['banana', 'milk'],
                'instructions': '1. Blend bananas with milk\n2. Serve cold',
                'preparation_time': 5
            }
        }
        return recipes
    
    def recommend_recipes(self, food_items):
        """
        Recommend recipes based on expiring food items
        
        Args:
            food_items (list): List of detected food items
            
        Returns:
            list: Recommended recipes
        """
        # Get expiring items (within 3 days)
        expiring_items = [item['name'] for item in food_items if item['days_until_expiry'] <= 3]
        
        # Find recipes that use these items
        recommended_recipes = []
        for recipe_key, recipe in self.recipe_database.items():
            # Check if recipe uses any expiring items
            if any(ingredient in expiring_items for ingredient in recipe['ingredients']):
                recommended_recipes.append(recipe)
        
        return recommended_recipes
    
    def get_recipe_details(self, recipe_name):
        """Get detailed information about a recipe"""
        return self.recipe_database.get(recipe_name, None)

# Example usage
if __name__ == "__main__":
    recommender = RecipeRecommender()
    
    # Sample food items (from image recognition)
    sample_items = [
        {'name': 'tomato', 'quantity': 3, 'days_until_expiry': 2},
        {'name': 'banana', 'quantity': 2, 'days_until_expiry': 1},
        {'name': 'bread', 'quantity': 1, 'days_until_expiry': 3},
        {'name': 'milk', 'quantity': 1, 'days_until_expiry': 5}
    ]
    
    recommendations = recommender.recommend_recipes(sample_items)
    print("Recommended recipes:")
    for recipe in recommendations:
        print(f"- {recipe['name']} (Prep time: {recipe['preparation_time']} mins)")