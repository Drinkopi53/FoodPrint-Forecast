"""
Prophet model for food waste prediction
"""
import pandas as pd
from prophet import Prophet
import numpy as np
import os

class FoodWastePredictor:
    def __init__(self):
        self.model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True
        )
        self.is_fitted = False
        self.training_data = None
    
    def prepare_data(self, csv_path='data/food_waste_sample.csv'):
        """
        Prepare data for Prophet model from CSV file
        
        Args:
            csv_path (str): Path to CSV file with historical waste data
            
        Returns:
            DataFrame: Prepared data for Prophet
        """
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df['ds'] = pd.to_datetime(df['ds'])
            self.training_data = df
            return df
        else:
            # Fallback to sample data generation if file doesn't exist
            print(f"Warning: {csv_path} not found. Generating sample data.")
            dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
            waste_amounts = np.random.poisson(lam=2.5, size=len(dates))  # Random waste data
            
            df = pd.DataFrame({
                'ds': dates,
                'y': waste_amounts
            })
            self.training_data = df
            return df
    
    def train_model(self, df=None):
        """
        Train the Prophet model
        
        Args:
            df (DataFrame): Training data. If None, uses data from prepare_data()
        """
        if df is None:
            if self.training_data is None:
                raise ValueError("No training data available. Call prepare_data() first.")
            df = self.training_data
            
        self.model.fit(df)
        self.is_fitted = True
    
    def predict_waste(self, periods=30):
        """
        Predict food waste for future periods
        
        Args:
            periods (int): Number of days to predict
            
        Returns:
            DataFrame: Predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be trained first")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    def calculate_waste_from_items(self, food_items):
        """
        Calculate potential waste based on detected food items
        
        Args:
            food_items (list): List of detected food items
            
        Returns:
            dict: Waste prediction information
        """
        # Calculate total potential waste
        total_items = sum([item['quantity'] for item in food_items])
        expiring_soon = sum([item['quantity'] for item in food_items if item['days_until_expiry'] <= 3])
        
        return {
            'total_items': total_items,
            'expiring_soon': expiring_soon,
            'estimated_waste_percentage': (expiring_soon / total_items) * 100 if total_items > 0 else 0
        }

# Example usage
if __name__ == "__main__":
    predictor = FoodWastePredictor()
    sample_data = predictor.prepare_data()
    print("Sample data for model training:")
    print(sample_data.head())
    
    # Train the model
    print("Training model...")
    predictor.train_model()
    
    # Make predictions
    forecast = predictor.predict_waste(periods=30)
    print("Waste prediction for next 30 days:")
    print(forecast[['ds', 'yhat']].tail(10))