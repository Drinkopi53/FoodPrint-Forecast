"""
Coordinator module that integrates all components of FoodPrint Forecast
"""
import os
from models.image_recognition import FridgeImageAnalyzer
from models.waste_predictor import FoodWastePredictor
from models.recipe_recommender import RecipeRecommender
from models.emission_calculator import EmissionCalculator
from models.leaderboard import Leaderboard

class FoodPrintForecast:
    def __init__(self):
        self.image_analyzer = FridgeImageAnalyzer()
        self.waste_predictor = FoodWastePredictor()
        self.recipe_recommender = RecipeRecommender()
        self.emission_calculator = EmissionCalculator()
        self.leaderboard = Leaderboard()
    
    def analyze_fridge_image(self, image_path):
        """
        Complete analysis of a fridge image
        
        Args:
            image_path (str): Path to the fridge image
            
        Returns:
            dict: Complete analysis results
        """
        # 1. Analyze image to detect food items
        food_items = self.image_analyzer.analyze_image(image_path)
        
        # 2. Predict waste based on detected items
        waste_prediction = self.waste_predictor.calculate_waste_from_items(food_items)
        
        # 3. Recommend recipes for expiring items
        recipes = self.recipe_recommender.recommend_recipes(food_items)
        
        # 4. Calculate avoided emissions
        emission_results = self.emission_calculator.calculate_avoided_emissions(food_items)
        
        # 5. Compile results
        results = {
            'detected_items': food_items,
            'waste_prediction': waste_prediction,
            'recommended_recipes': recipes,
            'emission_results': emission_results
        }
        
        return results
    
    def add_user_contribution(self, username, emission_results):
        """
        Add user's contribution to leaderboard
        
        Args:
            username (str): User's name
            emission_results (dict): Results from emission calculation
        """
        self.leaderboard.add_user_contribution(
            username, 
            emission_results['avoided_emissions_kg'], 
            emission_results['items_saved']
        )
    
    def get_leaderboard(self, limit=10):
        """
        Get community leaderboard
        
        Args:
            limit (int): Number of top users to return
            
        Returns:
            list: Top users on leaderboard
        """
        return self.leaderboard.get_top_users(limit)

# Example usage
if __name__ == "__main__":
    system = FoodPrintForecast()
    
    # For demonstration, we'll simulate the image analysis
    # In a real implementation, this would use an actual image file
    print("Analyzing fridge contents...")
    
    # Simulate detected items (normally from image_analyzer.analyze_image)
    sample_items = [
        {'name': 'tomato', 'quantity': 3, 'days_until_expiry': 2},
        {'name': 'banana', 'quantity': 2, 'days_until_expiry': 1},
        {'name': 'bread', 'quantity': 1, 'days_until_expiry': 3},
        {'name': 'milk', 'quantity': 1, 'days_until_expiry': 5}
    ]
    
    # Simulate waste prediction
    waste_pred = system.waste_predictor.calculate_waste_from_items(sample_items)
    print(f"Waste prediction: {waste_pred['expiring_soon']} items expiring soon out of {waste_pred['total_items']} total")
    
    # Get recipe recommendations
    recipes = system.recipe_recommender.recommend_recipes(sample_items)
    print(f"Found {len(recipes)} recipes for expiring items:")
    for recipe in recipes:
        print(f"  - {recipe['name']}")
    
    # Calculate emissions
    emissions = system.emission_calculator.calculate_avoided_emissions(sample_items)
    print(f"Emissions that can be avoided: {emissions['avoided_emissions_kg']} kg CO2")
    
    # Add to leaderboard (as example)
    system.add_user_contribution("Alice", emissions)
    
    # Show leaderboard
    top_users = system.get_leaderboard()
    print("\nTop contributors:")
    for i, user in enumerate(top_users, 1):
        print(f"{i}. {user['username']}: {user['total_emissions_avoided']:.1f} kg CO2 avoided")