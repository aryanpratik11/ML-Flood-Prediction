# ML Driven Flood Prediction and Impact Analysis Using Multi-Factor Data Integration for Bihar Floods

This project uses machine learning models to predict flood severity and estimate damage to area, population, crops, and houses in Bihar, India. It is built using Python, XGBoost, Flask (backend), and React (frontend).

---

## 📁 Project Structure

```
ML-Flood-Prediction/
├── data/                  # Datasets and preprocessed files
├── models/                # Saved ML models and scalers
├── src/                   # Model training and inference scripts
├── website/
│   ├── backend/           # Flask backend API
│   └── frontend/          # React frontend interface
├── docs/                  # Confusion matrix, feature plots & final report
└── README.md             
```

---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/aryanpratik11/ML-Flood-Prediction.git
cd ML-Flood-Prediction
```

### 2. Set Up the Backend (Flask API)

```bash
cd website/backend
pip install -r requirements.txt
python app.py
```

* This starts a server at: `http://127.0.0.1:5000/predict`
* Make sure `../models/` folder has all `.pkl` model and scaler files.

### 3. Set Up the Frontend (React UI)

```bash
cd ../frontend
npm install
npm start
```

* Open: `http://localhost:3000`
* Select district, river, rainfall and level to predict flood severity and damage.


---

## 📄 Project Report

View the full report with technical details:

> 📓 [Click to View Report](./report/Minor_Project_Report.pdf)


---

## 🛠️ Tools & Technologies

* Python (pandas, numpy, scikit-learn, xgboost)
* Flask for API
* React for frontend
* joblib for model serialization
* Git & GitHub for version control

---

## 📢 Authors

* Aryan Pratik \[CS22B1010]
* Aditya Gupta \[CS22B1003]

Supervised by Dr. Kiran Reddy, IIIT Raichur

---

## 🌐 License

This project is for academic use only.

---
