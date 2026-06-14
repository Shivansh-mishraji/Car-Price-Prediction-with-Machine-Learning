from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
import sys

# Add src to Python path so we can import our inference module
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.append(current_dir)

try:
    from src.inference import CarPricePredictor
except ImportError as e:
    print(f"Error importing inference module: {e}")
    # Fallback to absolute if needed
    sys.path.append(src_dir)
    from inference import CarPricePredictor

app = FastAPI(
    title="Car Price Prediction API",
    description="API to predict the selling price of a car based on its features.",
    version="1.0.0"
)

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
try:
    predictor = CarPricePredictor()
except Exception as e:
    print(f"Warning: Model not loaded yet. Make sure to run src/train.py first. Error: {e}")
    predictor = None

class CarFeatures(BaseModel):
    Year: int
    Present_Price: float
    Driven_kms: int
    Fuel_Type: str
    Selling_type: str
    Transmission: str
    Owner: int

@app.post("/predict")
def predict_price(features: CarFeatures):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. Please train the model first.")
        
    try:
        predicted_price = predictor.predict(
            year=features.Year,
            present_price=features.Present_Price,
            driven_kms=features.Driven_kms,
            fuel_type=features.Fuel_Type,
            selling_type=features.Selling_type,
            transmission=features.Transmission,
            owner=features.Owner
        )
        # Price is typically predicted in Lakhs according to the dataset context
        return {
            "predicted_price_lakhs": round(predicted_price, 2),
            "currency": "INR Lakhs"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": predictor is not None}

# Mount the frontend static files
frontend_dir = os.path.join(current_dir, "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def serve_frontend():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to Car Price Prediction API. Frontend not found at /frontend/index.html"}

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
