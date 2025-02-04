from fastapi import FastAPI

import pandas as pd

app = FastAPI()

@app.get("/data_collection")
def data_collection():
    pass

@app.get("/data_cleaning")
def data_cleaning():
    pass

@app.get("/predict")
def predict(user_id: int):
    # Load the data by using Twitter API
    # Predict the score based on the data
    result = {'user_id': user_id, "score": 0.5}
    return result

