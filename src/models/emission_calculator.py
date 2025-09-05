"""
Module to calculate avoided carbon emissions
"""
class EmissionCalculator:
    def __init__(self):
        # Carbon footprint data (kg CO2 equivalent per kg of food)
        # Source: https://www.sciencedirect.com/science/article/pii/S0959652616303584
        self.carbon_footprints = {
            'tomato': 1.1,  # kg CO2/kg
            'banana': 0.9,
            'apple': 0.5,
            'milk': 1.5,
            'bread': 1.0,
            'egg': 0.8,
            'chicken': 3.2,
            'lettuce': 0.3,
            'rice': 2.7,
            'pasta': 1.2,
            'cheese': 8.5,
            'beef': 27.0,
            'pork': 6.1,
            'fish': 3.9
        }
    
    def calculate_avoided_emissions(self, food_items, recipes_used=None):
        """
        Calculate the carbon emissions avoided by using expiring food
        
        Args:
            food_items (list): List of food items that were about to expire
            recipes_used (list): List of recipes that were used (optional)
            
        Returns:
            dict: Emission calculation results
        """
        # Calculate emissions for expiring items (would be wasted)
        expiring_items = [item for item in food_items if item['days_until_expiry'] <= 3]
        avoided_emissions = 0
        
        for item in expiring_items:
            food_name = item['name']
            quantity = item['quantity']
            
            # Get carbon footprint per item (simplified)
            # In a real implementation, we would consider item weight
            footprint = self.carbon_footprints.get(food_name, 1.0)
            avoided_emissions += footprint * quantity
        
        # Calculate total items and percentage
        total_items = sum([item['quantity'] for item in food_items])
        expiring_count = sum([item['quantity'] for item in expiring_items])
        
        return {
            'avoided_emissions_kg': round(avoided_emissions, 2),
            'items_saved': expiring_count,
            'total_items': total_items,
            'waste_prevented_percentage': (expiring_count / total_items) * 100 if total_items > 0 else 0
        }
    
    def get_food_footprint(self, food_name):
        """Get the carbon footprint of a specific food item"""
        return self.carbon_footprints.get(food_name, 1.0)

# Example usage
if __name__ == "__main__":
    calculator = EmissionCalculator()
    
    # Sample food items
    sample_items = [
        {'name': 'tomato', 'quantity': 3, 'days_until_expiry': 2},
        {'name': 'banana', 'quantity': 2, 'days_until_expiry': 1},
        {'name': 'bread', 'quantity': 1, 'days_until_expiry': 3},
        {'name': 'milk', 'quantity': 1, 'days_until_expiry': 5}
    ]
    
    results = calculator.calculate_avoided_emissions(sample_items)
    print("Emission calculation results:")
    print(f"Avoided emissions: {results['avoided_emissions_kg']} kg CO2")
    print(f"Items saved from waste: {results['items_saved']} out of {results['total_items']}")
    print(f"Waste prevented: {results['waste_prevented_percentage']:.1f}%")