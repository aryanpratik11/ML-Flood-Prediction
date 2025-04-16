import os
from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Dynamically get absolute path to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load models and scalers
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


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Feature engineering
    data['rainfall_river'] = data['Rainfall (mm)'] * data['River Level']
    data['rainfall_district'] = data['Rainfall (mm)'] * data['District']
    data['riverlevel_district'] = data['River Level'] * data['District']

    # Feature order
    X = pd.DataFrame([data])[[
        'District', 'Rainfall (mm)', 'River', 'River Level',
        'rainfall_river', 'rainfall_district', 'riverlevel_district'
    ]]

    # Predict
    flood_risk = int(models['flood_risk'].predict(X)[0])
    area = float(np.expm1(models['area'].predict(X))[0])
    population = float(np.expm1(models['population'].predict(X))[0])
    crops = float(np.expm1(models['crops'].predict(X))[0])
    houses = float(np.expm1(models['houses'].predict(X))[0])

    return jsonify({
        "Flood Risk": flood_risk,
        "Area affected (m.ha)": area,
        "Population affected (million)": population,
        "Damage to Crops": crops,
        "Damage to Houses": houses
    })

if __name__ == "__main__":
    app.run(debug=True)
