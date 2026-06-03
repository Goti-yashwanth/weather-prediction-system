import pandas as pd
import pickle
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# LOAD DATA

df = pd.read_csv("datasets/weather.csv")

# KEEP REQUIRED COLUMNS

df = df[[
    'MinTemp',
    'MaxTemp',
    'Rainfall',
    'Humidity9am',
    'Humidity3pm',
    'Pressure9am',
    'Pressure3pm',
    'Temp9am',
    'Temp3pm',
    'RainToday',
    'RainTomorrow'
]]

# REMOVE NULL VALUES

df.dropna(inplace=True)

# ENCODE

le = LabelEncoder()

df['RainToday'] = le.fit_transform(df['RainToday'])
df['RainTomorrow'] = le.fit_transform(df['RainTomorrow'])

# FEATURES

X = df.drop(
    'RainTomorrow',
    axis=1
)

y = df['RainTomorrow']

# SCALING

scaler = StandardScaler()

X = scaler.fit_transform(X)

joblib.dump(
    scaler,
    "scaler.pkl"
)

# SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# MODEL

model = DecisionTreeClassifier(
    random_state=42
)

model.fit(
    X_train,
    y_train
)

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)

# SAVE MODEL

pickle.dump(
    model,
    open("model.pkl", "wb")
)

print("Model Saved Successfully")