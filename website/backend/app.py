import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load models (update paths if needed)
try:
    models = {
        'flood_risk': joblib.load(os.path.join(MODEL_DIR, "xgb_flood_risk_model.pkl")),
        'area': joblib.load(os.path.join(MODEL_DIR, "xgb_area_model.pkl")),
        'population': joblib.load(os.path.join(MODEL_DIR, "xgb_population_model.pkl")),
        'crops': joblib.load(os.path.join(MODEL_DIR, "xgb_crops_model.pkl")),
        'houses': joblib.load(os.path.join(MODEL_DIR, "xgb_houses_model.pkl"))
    }
    print("✅ Models loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    raise

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Validate input
        required = ['District', 'Rainfall (mm)', 'River', 'River Level']
        if not all(field in data for field in required):
            return jsonify({"error": "Missing required fields"}), 400

        # Feature engineering
        data['rainfall_river'] = data['Rainfall (mm)'] * data['River Level']
        data['rainfall_district'] = data['Rainfall (mm)'] * data['District']
        data['riverlevel_district'] = data['River Level'] * data['District']

        # Predict
        X = pd.DataFrame([data])
        predictions = {
            "Flood_Risk": int(models['flood_risk'].predict(X)[0]),
            "Area_affected": round(float(models['area'].predict(X)[0]), 2),
            "Population_affected": round(float(models['population'].predict(X)[0]), 2),
            "crop_damage":round(float(models['crops'].predict(X)[0]),2),
            "houses_damage":round(float(models['houses'].predict(X)[0]),2),
            "timestamp": datetime.now().isoformat()
        }
        return jsonify(predictions)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)