import streamlit as st
import pandas as pd
import pickle
import joblib
import plotly.express as px
import os

from weather_api import get_current_weather, get_forecast
from utils import save_prediction_history

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Weather Prediction System",
    page_icon="🌦",
    layout="wide"
)
st.markdown("""
<style>
.stApp{
    background-color:#0E1117;
    color:white;
}
h1,h2,h3{
    color:#00D4FF;
}
</style>
""", unsafe_allow_html=True)
# -------------------------
# LOAD MODEL
# -------------------------

try:
    model = pickle.load(open("model.pkl", "rb"))
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    st.error(f"Error loading model/scaler: {e}")
    st.stop()

# -------------------------
# TITLE
# -------------------------

st.markdown("""
<h1 style='text-align:center;color:skyblue'>
🌦 AI Weather Prediction System
</h1>
""", unsafe_allow_html=True)

st.write("---")

# -------------------------
# SIDEBAR
# -------------------------

menu = st.sidebar.radio(
    "Navigation",
    [
        "Current Weather",
        "Rain Prediction",
        "7-Day Forecast",
        "Analytics",
        "Bulk Prediction",
        "Prediction History"
    ]
)

# -------------------------
# CURRENT WEATHER
# -------------------------

if menu == "Current Weather":

    st.subheader("🌍 Live Weather")

    city = st.text_input(
        "Enter City Name",
        "Hyderabad"
    )

    if st.button("Get Weather"):

        try:
            weather = get_current_weather(city)

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Temperature",
                f"{weather['temperature']} °C"
            )

            c2.metric(
                "Humidity",
                f"{weather['humidity']} %"
            )

            c3.metric(
                "Pressure",
                f"{weather['pressure']} hPa"
            )

            c4.metric(
                "Wind Speed",
                f"{weather['wind_speed']} m/s"
            )

            st.success(
                f"Condition: {weather['condition']}"
            )

            if weather["condition"] == "Rain":
                st.image(
                    "https://openweathermap.org/img/wn/10d@2x.png"
                )

            elif weather["condition"] == "Clouds":
                st.image(
                    "https://openweathermap.org/img/wn/03d@2x.png"
                )

            else:
                st.image(
                    "https://openweathermap.org/img/wn/01d@2x.png"
                )

        except Exception as e:
            st.error(f"Error: {e}")

# -------------------------
# RAIN PREDICTION
# -------------------------

elif menu == "Rain Prediction":

    st.subheader("🤖 Predict Rain")

    city = st.text_input(
        "Enter City",
        "Hyderabad"
    )

    if st.button("Predict Weather"):

        try:

            weather = get_current_weather(city)

            data = pd.DataFrame({

                'MinTemp': [weather['temperature'] - 2],
                'MaxTemp': [weather['temperature'] + 2],
                'Rainfall': [0],
                'Humidity9am': [weather['humidity']],
                'Humidity3pm': [weather['humidity']],
                'Pressure9am': [weather['pressure']],
                'Pressure3pm': [weather['pressure']],
                'Temp9am': [weather['temperature']],
                'Temp3pm': [weather['temperature']],
                'RainToday': [
                    1 if weather['condition'] == "Rain" else 0
                ]
            })

            scaled_data = scaler.transform(data)

            prediction = model.predict(
                scaled_data
            )

            probability = model.predict_proba(
                scaled_data
            )

            rain_probability = round(
                probability[0][1] * 100,
                2
            )

            st.subheader("📊 Rain Probability")

            st.progress(
                int(rain_probability)
            )

            st.info(
                f"Rain Chance: {rain_probability}%"
            )

            if rain_probability < 30:
                st.success("🟢 Low Rain Risk")

            elif rain_probability < 70:
                st.warning("🟡 Moderate Rain Risk")

            else:
                st.error("🔴 High Rain Risk")

            if prediction[0] == 1:

                st.success(
                    "🌧 Rain Expected Tomorrow"
                )

                result = "Rain"

            else:

                st.warning(
                    "☀ No Rain Expected Tomorrow"
                )

                result = "No Rain"

            save_prediction_history(
                city,
                result,
                rain_probability
            )

            chart_df = pd.DataFrame({

                "Weather Metrics": [
                    "Temperature",
                    "Humidity",
                    "Pressure"
                ],

                "Values": [
                    weather['temperature'],
                    weather['humidity'],
                    weather['pressure']
                ]
            })

            fig = px.bar(
                chart_df,
                x="Weather Metrics",
                y="Values",
                text="Values",
                title="🌦 Weather Analytics"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Prediction Error: {e}")

# -------------------------
# 7-DAY FORECAST
# -------------------------

elif menu == "7-Day Forecast":

    st.subheader(
        "📅 Weather Forecast"
    )

    city = st.text_input(
        "Enter City",
        "Hyderabad",
        key="forecast_city"
    )

    if st.button("Get Forecast"):

        try:

            forecast = get_forecast(city)

            forecast_list = forecast["list"][:10]

            forecast_data = []

            for item in forecast_list:

                forecast_data.append({

                    "Date": item["dt_txt"],
                    "Temperature": item["main"]["temp"],
                    "Humidity": item["main"]["humidity"]

                })

            forecast_df = pd.DataFrame(
                forecast_data
            )

            st.dataframe(
                forecast_df
            )

            fig = px.line(
                forecast_df,
                x="Date",
                y="Temperature",
                title="📅 Temperature Forecast"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Forecast Error: {e}")

# -------------------------
# ANALYTICS
# -------------------------

elif menu == "Analytics":

    st.subheader(
        "📊 Weather Analytics"
    )

    analytics_df = pd.DataFrame({

        "Metric": [
            "Temperature",
            "Humidity",
            "Pressure"
        ],

        "Value": [
            32,
            44,
            1008
        ]

    })

    fig = px.pie(
        analytics_df,
        values="Value",
        names="Metric",
        title="Weather Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------
# BULK PREDICTION
# -------------------------

elif menu == "Bulk Prediction":

    st.subheader(
        "📂 Bulk Prediction"
    )

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            df = pd.read_csv(
                uploaded_file
            )

            st.write(
                "Uploaded Data"
            )

            st.dataframe(
                df.head()
            )

            st.success(
                "File Uploaded Successfully"
            )

        except Exception as e:
            st.error(f"CSV Error: {e}")

# -------------------------
# PREDICTION HISTORY
# -------------------------

elif menu == "Prediction History":

    st.subheader(
        "📜 Prediction History"
    )

    try:

        history = pd.read_csv(
            "prediction_history.csv"
        )

        st.dataframe(
            history
        )

        if len(history) > 0:

            st.bar_chart(
                history["Probability"]
            )

    except Exception:

        st.warning(
            "No Prediction History Found"
        )

# -------------------------
# FOOTER
# -------------------------

st.write("---")

st.caption(
    "Created using Python • Streamlit • Decision Tree • OpenWeatherMap API"
)