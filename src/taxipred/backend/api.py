from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from typing import Literal
import joblib
import numpy as np
from taxipred.utils.constants import PREDICTION_DATA_FILE, ORIGINAL_DATA_FILE
from taxipred.utils.constants import MODEL_PATH, SCALER_PATH


app = FastAPI()

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


class TaxiTrip(BaseModel):
    Trip_Distance_km: float
    Trip_Duration_Minutes: float
    Traffic_Encoded: Literal[0,1,2]

@app.get("/data/data")
def get_original_data():

    df = pd.read_csv(ORIGINAL_DATA_FILE)

    return df.to_dict(orient="records")

@app.get("/data/predictions")
def get_predictions_data():

    df = pd.read_csv(PREDICTION_DATA_FILE)

    df_limited = df.head(20)

    return df_limited.to_dict(orient="records")


@app.post("/predict")
def predict_price(trip: TaxiTrip):
    data = trip.model_dump()
    
    raw_features = np.array([
        data['Trip_Distance_km'],
        data['Trip_Duration_Minutes'],
        data['Traffic_Encoded']

    ]).reshape(1, -1)

    scaled_features = scaler.transform(raw_features)

    prediction = model.predict(scaled_features)

    return {
        "predicted price": round(float(prediction), 2)
    }





    