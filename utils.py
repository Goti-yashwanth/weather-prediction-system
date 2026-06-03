import pandas as pd
from datetime import datetime

def save_prediction_history(
city,
prediction,
probability
):

    history = pd.DataFrame({

        "Date":[datetime.now()],
        "City":[city],
        "Prediction":[prediction],
        "Probability":[probability]

    })

    history.to_csv(

        "prediction_history.csv",

        mode="a",
        header=False,
        index=False

    )