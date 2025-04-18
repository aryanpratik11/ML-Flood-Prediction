# src/preprocess.py
import pandas as pd
import numpy as np
import joblib

def preprocess_data(data_input, scaler_models):
    # Add engineered features
    data_input['rainfall_river'] = data_input['Rainfall (mm)'] * data_input['River Level']
    data_input['rainfall_district'] = data_input['Rainfall (mm)'] * data_input['District']
    data_input['riverlevel_district'] = data_input['River Level'] * data_input['District']
    
    # Feature order (must match training WITHOUT 'Year-Month')
    X_new = pd.DataFrame([data_input])[[ 
        'District', 'Rainfall (mm)', 'River', 'River Level',
        'rainfall_river', 'rainfall_district', 'riverlevel_district'
    ]]
    
    # Scale the features using saved scalers
    scaled_data = {}
    for target, scaler in scaler_models.items():
        scaled_data[target] = scaler.transform(X_new)
    
    return scaled_data