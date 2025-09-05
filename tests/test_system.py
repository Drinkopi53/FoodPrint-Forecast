"""
Test script for FoodPrint Forecast components
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.coordinator import FoodPrintForecast

def test_system():
    """Test the complete FoodPrint Forecast system"""
    print("Testing FoodPrint Forecast system...")
    
    # Initialize the system
    system = FoodPrintForecast()
    
    # Test image analysis (using mock data)
    print("\n1. Testing image analysis...")
    # In a real implementation, we would use an actual image file
    # For testing, we'll simulate the results
    sample_items = [
        {'name': 'tomato', 'quantity': 3, 'days_until_expiry': 2},
        {'name': 'banana', 'quantity': 2, 'days_until_expiry': 1},
        {'name': 'bread', 'quantity': 1, 'days_until_expiry': 3},
        {'name': 'milk', 'quantity': 1, 'days_until_expiry': 5}
    ]
    
    print("Detected items:")
    for item in sample_items:
        status = " (EXPIRING SOON!)" if item['days_until_expiry'] <= 3 else ""
        print(f"- {item['name']}: {item['quantity']} items, expires in {item['days_until_expiry']} days{status}")
    
    # Test waste prediction
    print("\n2. Testing waste prediction...")
    waste_pred = system.waste_predictor.calculate_waste_from_items(sample_items)
    print(f"Total items: {waste_pred['total_items']}")
    print(f"Expiring soon: {waste_pred['expiring_soon']}")
    print(f"Estimated waste percentage: {waste_pred['estimated_waste_percentage']:.1f}%")
    
    # Test recipe recommendation
    print("\n3. Testing recipe recommendation...")
    recipes = system.recipe_recommender.recommend_recipes(sample_items)
    print(f"Found {len(recipes)} recipes for expiring items:")
    for recipe in recipes:
        print(f"- {recipe['name']} (Prep time: {recipe['preparation_time']} mins)")
    
    # Test emission calculation
    print("\n4. Testing emission calculation...")
    emissions = system.emission_calculator.calculate_avoided_emissions(sample_items)
    print(f"Avoided emissions: {emissions['avoided_emissions_kg']} kg CO2")
    print(f"Items saved from waste: {emissions['items_saved']} out of {emissions['total_items']}")
    print(f"Waste prevented: {emissions['waste_prevented_percentage']:.1f}%")
    
    # Test leaderboard
    print("\n5. Testing leaderboard...")
    # Add some sample contributions
    system.add_user_contribution("Alice", emissions)
    system.add_user_contribution("Bob", {'avoided_emissions_kg': 3.2, 'items_saved': 4})
    system.add_user_contribution("Charlie", {'avoided_emissions_kg': 7.8, 'items_saved': 10})
    system.add_user_contribution("Alice", {'avoided_emissions_kg': 2.1, 'items_saved': 3})  # Second contribution
    
    # Display leaderboard
    top_users = system.get_leaderboard()
    print("Top contributors:")
    for i, user in enumerate(top_users, 1):
        print(f"{i}. {user['username']}: {user['total_emissions_avoided']:.1f} kg CO2 avoided")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_system()