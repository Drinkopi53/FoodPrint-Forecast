"""
Main application file for FoodPrint Forecast
"""
import os
import sys
import argparse

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.coordinator import FoodPrintForecast

def main():
    parser = argparse.ArgumentParser(description="FoodPrint Forecast - Sistem Prediksi Limbah Pangan Rumah Tangga")
    parser.add_argument("--web", action="store_true", help="Run the web application")
    parser.add_argument("--image", type=str, help="Path to fridge image for analysis")
    parser.add_argument("--username", type=str, help="Username for leaderboard contribution")
    
    args = parser.parse_args()
    
    if args.web:
        # Run web application
        from src.web.app import app
        print("Starting FoodPrint Forecast web application...")
        print("Visit http://localhost:5000 in your browser")
        app.run(debug=True)
    elif args.image:
        # Analyze image from command line
        if not os.path.exists(args.image):
            print(f"Error: Image file {args.image} not found")
            return
        
        system = FoodPrintForecast()
        print("Analyzing fridge contents...")
        
        try:
            results = system.analyze_fridge_image(args.image)
            
            print("\nDetected items:")
            for item in results['detected_items']:
                status = " (EXPIRING SOON!)" if item['days_until_expiry'] <= 3 else ""
                print(f"- {item['name']}: {item['quantity']} items, expires in {item['days_until_expiry']} days{status}")
            
            print(f"\nWaste prediction:")
            print(f"- {results['waste_prediction']['expiring_soon']} items expiring soon out of {results['waste_prediction']['total_items']} total")
            print(f"- Estimated waste: {results['waste_prediction']['estimated_waste_percentage']:.1f}%")
            
            print(f"\nRecommended recipes:")
            for recipe in results['recommended_recipes']:
                print(f"- {recipe['name']} (Prep time: {recipe['preparation_time']} mins)")
            
            print(f"\nEnvironmental impact:")
            print(f"- Emissions that can be avoided: {results['emission_results']['avoided_emissions_kg']} kg CO2")
            print(f"- Items saved from waste: {results['emission_results']['items_saved']} out of {results['emission_results']['total_items']}")
            print(f"- Waste prevented: {results['emission_results']['waste_prevented_percentage']:.1f}%")
            
            # Add to leaderboard if username provided
            if args.username:
                system.add_user_contribution(args.username, results['emission_results'])
                print(f"\nAdded contribution for user: {args.username}")
                
                # Show leaderboard
                print("\nTop contributors:")
                top_users = system.get_leaderboard()
                for i, user in enumerate(top_users, 1):
                    print(f"{i}. {user['username']}: {user['total_emissions_avoided']:.1f} kg CO2 avoided")
            
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
    else:
        # Show help
        print("FoodPrint Forecast - Sistem Prediksi Limbah Pangan Rumah Tangga")
        print("=" * 60)
        print("Usage:")
        print("  python src/main.py --web              # Run web application")
        print("  python src/main.py --image <path>     # Analyze fridge image")
        print("  python src/main.py --image <path> --username <name>  # Analyze and contribute to leaderboard")
        print("=" * 60)
        print("\nFeatures:")
        print("1. Prediksi limbah pangan berdasarkan foto isi kulkas")
        print("2. Rekomendasi resep untuk bahan yang akan kadaluarsa")
        print("3. Perhitungan emisi karbon yang berhasil dihindari")
        print("4. Leaderboard komunitas")

if __name__ == "__main__":
    main()