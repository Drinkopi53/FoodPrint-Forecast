"""
Community leaderboard system
"""
import json
import os
from datetime import datetime

class Leaderboard:
    def __init__(self, data_file='data/leaderboard.json'):
        self.data_file = data_file
        self.leaderboard = self._load_leaderboard()
    
    def _load_leaderboard(self):
        """Load leaderboard data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        else:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            return []
    
    def _save_leaderboard(self):
        """Save leaderboard data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.leaderboard, f, indent=2)
    
    def add_user_contribution(self, username, avoided_emissions, items_saved):
        """
        Add a user's contribution to the leaderboard
        
        Args:
            username (str): User's name
            avoided_emissions (float): Amount of emissions avoided in kg CO2
            items_saved (int): Number of items saved from waste
        """
        # Check if user already exists
        user_found = False
        for entry in self.leaderboard:
            if entry['username'] == username:
                # Update existing user's stats
                entry['total_emissions_avoided'] += avoided_emissions
                entry['total_items_saved'] += items_saved
                entry['contributions'] += 1
                entry['last_contribution'] = datetime.now().isoformat()
                user_found = True
                break
        
        # Add new user if not found
        if not user_found:
            new_entry = {
                'username': username,
                'total_emissions_avoided': avoided_emissions,
                'total_items_saved': items_saved,
                'contributions': 1,
                'last_contribution': datetime.now().isoformat()
            }
            self.leaderboard.append(new_entry)
        
        # Sort by emissions avoided (descending)
        self.leaderboard.sort(key=lambda x: x['total_emissions_avoided'], reverse=True)
        
        # Save updated leaderboard
        self._save_leaderboard()
    
    def get_top_users(self, limit=10):
        """
        Get top users from the leaderboard
        
        Args:
            limit (int): Number of top users to return
            
        Returns:
            list: Top users sorted by emissions avoided
        """
        return self.leaderboard[:limit]
    
    def get_user_rank(self, username):
        """
        Get a specific user's rank
        
        Args:
            username (str): User's name
            
        Returns:
            int: User's rank (1-indexed) or None if user not found
        """
        for i, entry in enumerate(self.leaderboard):
            if entry['username'] == username:
                return i + 1
        return None

# Example usage
if __name__ == "__main__":
    leaderboard = Leaderboard()
    
    # Add some sample contributions
    leaderboard.add_user_contribution("Alice", 5.2, 8)
    leaderboard.add_user_contribution("Bob", 3.7, 5)
    leaderboard.add_user_contribution("Charlie", 7.1, 12)
    leaderboard.add_user_contribution("Alice", 2.3, 3)  # Alice's second contribution
    
    print("Top contributors:")
    top_users = leaderboard.get_top_users(5)
    for i, user in enumerate(top_users, 1):
        print(f"{i}. {user['username']}: {user['total_emissions_avoided']:.1f} kg CO2 avoided")