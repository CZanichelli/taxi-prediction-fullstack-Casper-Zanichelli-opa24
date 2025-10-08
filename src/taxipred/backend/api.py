from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from taxipred.backend.data_processing import TaxiData

app = FastAPI()

taxi_data = TaxiData()

class TaxiTrip(BaseModel):
    Trip_Distance_km: float
    Trip_Duration_Minutes: float
    Traffic_Encoded: Literal[0,1,2]



@app.get("/taxi/")
async def read_taxi_data():
    return taxi_data.to_json()
    