import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import datetime

def get_data_path():
    # Looking for 'car data.csv' in the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, 'car data.csv')

def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    # Drop Car_Name as it has too many unique values and little predictive power without NLP
    if 'Car_Name' in df.columns:
        df = df.drop('Car_Name', axis=1)
        
    # Feature Engineering: Convert Year to Age
    current_year = datetime.datetime.now().year
    df['Age'] = current_year - df['Year']
    df = df.drop('Year', axis=1)
    
    # Separate features and target
    X = df.drop('Selling_Price', axis=1)
    y = df['Selling_Price']
    
    return X, y

def build_pipeline():
    # Define categorical and numerical columns
    categorical_cols = ['Fuel_Type', 'Selling_type', 'Transmission']
    numerical_cols = ['Present_Price', 'Driven_kms', 'Owner', 'Age']
    
    # Preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_cols)
        ]
    )
    
    # Model pipeline
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    return pipeline

def main():
    print("Starting Training Pipeline...")
    
    data_path = get_data_path()
    df = load_data(data_path)
    
    print(f"Data loaded successfully. Shape: {df.shape}")
    
    X, y = preprocess_data(df)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Building and training the model...")
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    
    # Evaluation
    predictions = pipeline.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    
    print("\n--- Model Evaluation ---")
    print(f"R2 Score: {r2:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    
    # Save the model
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    models_dir = os.path.join(project_root, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"\nModel saved successfully at: {model_path}")

if __name__ == "__main__":
    main()
