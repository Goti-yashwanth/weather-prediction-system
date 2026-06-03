# 🌦 AI Weather Prediction System

A Machine Learning based Weather Prediction System built using:

- Python
- Streamlit
- Decision Tree Classifier
- OpenWeatherMap API
- Plotly

## Features

- Live Weather Data
- Rain Prediction
- Rain Probability
- 7-Day Forecast
- Feature Importance
- Prediction History
- Interactive Charts
- Bulk CSV Upload

## Installation

```bash
pip install -r requirements.txt

RUN
python train_model.py
python -m streamlit run app.py

Dataset

Rain in Australia Dataset

Author

Yashwanth


---

### Before Pushing

Make sure these files exist:

```text
weather_prediction_system/
│
├── app.py
├── train_model.py
├── weather_api.py
├── utils.py
├── requirements.txt
├── README.md
├── model.pkl
├── scaler.pkl
├── prediction_history.csv
│
├── datasets/
│   └── weather.csv
