from fastapi import FastAPI
import mlflow
import mlflow.sklearnq
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/predict")
def predict(user_id: int):
    # Load the data by using Twitter API
    # Predict the score based on the data
    result = {'user_id': user_id, "score": 0.5}
    return result

