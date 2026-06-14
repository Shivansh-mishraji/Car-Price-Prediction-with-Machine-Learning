import os
import joblib
import pandas as pd
import datetime

class CarPricePredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            model_path = os.path.join(project_root, 'models', 'model.pkl')
            
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please run train.py first.")
            
        self.model = joblib.load(model_path)
        
    def predict(self, year: int, present_price: float, driven_kms: int, 
                fuel_type: str, selling_type: str, transmission: str, owner: int):
        """
        Predict the selling price of a car.
        """
        # Feature Engineering: Convert Year to Age
        current_year = datetime.datetime.now().year
        age = current_year - year
        
        # Create a DataFrame matching the expected training input
        input_data = pd.DataFrame([{
            'Present_Price': present_price,
            'Driven_kms': driven_kms,
            'Fuel_Type': fuel_type,
            'Selling_type': selling_type,
            'Transmission': transmission,
            'Owner': owner,
            'Age': age
        }])
        
        # Predict using the loaded pipeline (which includes preprocessing)
        prediction = self.model.predict(input_data)
        
        return float(prediction[0])

if __name__ == "__main__":
    # Simple test
    try:
        predictor = CarPricePredictor()
        # Sample test with dummy values
        price = predictor.predict(
            year=2015, 
            present_price=5.59, 
            driven_kms=27000, 
            fuel_type='Petrol', 
            selling_type='Dealer', 
            transmission='Manual', 
            owner=0
        )
        print(f"Predicted Price: {price:.2f} Lakhs")
    except Exception as e:
        print(f"Error during inference: {e}")
