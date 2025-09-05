"""
Data preparation script for generating sample training data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    """Generate sample food waste data for training the Prophet model"""
    
    # Create date range for a year
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate synthetic waste data
    # Base trend with some seasonality and noise
    np.random.seed(42)  # For reproducible results
    
    # Base level with weekly pattern
    base_waste = 5
    weekly_pattern = np.sin(2 * np.pi * np.arange(len(date_range)) / 7) * 2
    trend = np.linspace(0, 2, len(date_range))  # Slight upward trend
    
    # Add random noise
    noise = np.random.normal(0, 1, len(date_range))
    
    # Combine components
    waste_amounts = base_waste + weekly_pattern + trend + noise
    
    # Ensure no negative values
    waste_amounts = np.maximum(waste_amounts, 0)
    
    # Create DataFrame
    df = pd.DataFrame({
        'ds': date_range,
        'y': waste_amounts
    })
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/food_waste_sample.csv', index=False)
    
    print(f"Generated sample data with {len(df)} records")
    print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")
    print(f"Average waste per day: {df['y'].mean():.2f} items")
    print(f"Max waste in a day: {df['y'].max():.2f} items")
    print(f"Min waste in a day: {df['y'].min():.2f} items")
    
    return df

def generate_food_database():
    """Generate a sample food database with carbon footprints"""
    
    food_data = {
        'name': ['Tomat', 'Pisang', 'Apel', 'Susu', 'Roti', 'Telur', 'Ayam', 'Selada', 'Beras', 'Pasta', 'Keju', 'Daging Sapi', 'Daging Babi', 'Ikan'],
        'english_name': ['tomato', 'banana', 'apple', 'milk', 'bread', 'egg', 'chicken', 'lettuce', 'rice', 'pasta', 'cheese', 'beef', 'pork', 'fish'],
        'shelf_life_days': [7, 5, 30, 7, 5, 21, 2, 3, 365, 730, 90, 3, 3, 2],
        'carbon_footprint_kg_co2_per_kg': [1.1, 0.9, 0.5, 1.5, 1.0, 0.8, 3.2, 0.3, 2.7, 1.2, 8.5, 27.0, 6.1, 3.9]
    }
    
    df = pd.DataFrame(food_data)
    df.to_csv('data/food_database.csv', index=False)
    
    print(f"Generated food database with {len(df)} items")
    return df

if __name__ == "__main__":
    print("Generating sample data for FoodPrint Forecast...")
    
    # Generate sample waste data
    waste_data = generate_sample_data()
    
    # Generate food database
    food_data = generate_food_database()
    
    print("\nSample of generated waste data:")
    print(waste_data.head(10))
    
    print("\nSample of generated food database:")
    print(food_data.head(10))
    
    print("\nData generation complete. Files saved to 'data' directory.")