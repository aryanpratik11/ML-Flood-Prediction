# src/train.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error
from xgboost import XGBClassifier, XGBRegressor
from sklearn.preprocessing import FunctionTransformer

# Load and preprocess data
df = pd.read_csv("../data/preproc.csv")
X = df.drop(columns=['Year-Month', 'Flood Risk', 'Area affected in (m.ha)', 'Population affected in (million)', 'Damage to Crops', 'Damage to Houses', 'Flood Occurred'])
y_risk = df["Flood Risk"]
y_area = df["Area affected in (m.ha)"].fillna(df["Area affected in (m.ha)"].median())
y_pop = df["Population affected in (million)"].fillna(df["Population affected in (million)"].median())
y_crops = df["Damage to Crops"].fillna(df["Damage to Crops"].median())
y_houses = df["Damage to Houses"].fillna(df["Damage to Houses"].median())

# Define log transformation scalers
log_transformer = FunctionTransformer(np.log1p, inverse_func=np.expm1, validate=True)

scalers = {
    "area": log_transformer,
    "population": log_transformer,
    "crops": log_transformer,
    "houses": log_transformer
}

y_area_scaled = scalers["area"].fit_transform(y_area.values.reshape(-1, 1))
y_pop_scaled = scalers["population"].fit_transform(y_pop.values.reshape(-1, 1))
y_crops_scaled = scalers["crops"].fit_transform(y_crops.values.reshape(-1, 1))
y_houses_scaled = scalers["houses"].fit_transform(y_houses.values.reshape(-1, 1))

# Save scalers
for name, scaler in scalers.items():
    joblib.dump(scaler, f"../models/scaler_{name}.pkl")

# Train and save models
X_train, X_test, y_risk_train, y_risk_test, y_area_train, y_area_test, y_pop_train, y_pop_test, y_crops_train, y_crops_test, y_houses_train, y_houses_test = train_test_split(
    X, y_risk, y_area_scaled, y_pop_scaled, y_crops_scaled, y_houses_scaled, test_size=0.2, random_state=42
)

param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.05, 0.1],
    'max_depth': [3, 6],
    'subsample': [0.7],
    'colsample_bytree': [0.7]
}

# Flood risk classification model
clf = GridSearchCV(XGBClassifier(random_state=42), param_grid, cv=3, scoring='accuracy', n_jobs=-1)
clf.fit(X_train, y_risk_train)
best_clf = clf.best_estimator_
joblib.dump(best_clf, "../models/xgb_flood_risk_model.pkl")

# Regression models
def train_and_save_regressor(X_train, y_train, X_test, y_test, target_name):
    reg = GridSearchCV(XGBRegressor(random_state=42), param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1)
    reg.fit(X_train, y_train)
    best_reg = reg.best_estimator_
    joblib.dump(best_reg, f"../models/xgb_{target_name}_model.pkl")

train_and_save_regressor(X_train, y_area_train, X_test, y_area_test, "area")
train_and_save_regressor(X_train, y_pop_train, X_test, y_pop_test, "population")
train_and_save_regressor(X_train, y_crops_train, X_test, y_crops_test, "crops")
train_and_save_regressor(X_train, y_houses_train, X_test, y_houses_test, "houses")
