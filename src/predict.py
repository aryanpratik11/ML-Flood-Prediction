# src/predict.py
import sys
import json
import joblib
import numpy as np
import os
from src.preprocess import preprocess_data

# Check if input is provided via command line
if len(sys.argv) > 1:
    data_input = json.loads(sys.argv[1])

# Set model directory
MODEL_DIR = "../models"

# Load models and scalers
try:
    models = {
        'flood_risk': joblib.load(os.path.join(MODEL_DIR, "xgb_flood_risk_model.pkl")),
        'area': joblib.load(os.path.join(MODEL_DIR, "xgb_area_model.pkl")),
        'population': joblib.load(os.path.join(MODEL_DIR, "xgb_population_model.pkl")),
        'crops': joblib.load(os.path.join(MODEL_DIR, "xgb_crops_model.pkl")),
        'houses': joblib.load(os.path.join(MODEL_DIR, "xgb_houses_model.pkl"))
    }

    scalers = {
        'area': joblib.load(os.path.join(MODEL_DIR, "scaler_area.pkl")),
        'population': joblib.load(os.path.join(MODEL_DIR, "scaler_population.pkl")),
        'crops': joblib.load(os.path.join(MODEL_DIR, "scaler_crops.pkl")),
        'houses': joblib.load(os.path.join(MODEL_DIR, "scaler_houses.pkl"))
    }

except FileNotFoundError as e:
    print(f"❌ Error loading model or scaler files: {e}")
    exit()

def make_predictions(data_input):
    # Preprocess data and scale it
    scaled_data = preprocess_data(data_input, scalers)
    
    # Make predictions using models
    flood_risk_pred = models['flood_risk'].predict(scaled_data['flood_risk'])[0]
    
    area_scaled = models['area'].predict(scaled_data['area'])
    pop_scaled = models['population'].predict(scaled_data['population'])
    crops_scaled = models['crops'].predict(scaled_data['crops'])
    houses_scaled = models['houses'].predict(scaled_data['houses'])
    
    # Inverse transform to original scale
    area_original = np.expm1(area_scaled[0])
    population_original = np.expm1(pop_scaled[0])
    crops_original = np.expm1(crops_scaled[0])
    houses_original = np.expm1(houses_scaled[0])
    
    return {
        'Flood Risk': flood_risk_pred,
        'Area affected (m.ha)': area_original,
        'Population affected (million)': population_original,
        'Damage to Crops': crops_original,
        'Damage to Houses': houses_original
    }

# Output predictions
result = make_predictions(data_input)
print(json.dumps(result))  # Send the result back to Node.js
