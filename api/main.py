from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/nhl-data")
async def get_external_data():
    df = pd.read_csv('api/US_NHL_TEAMS.csv')
    return df.to_dict(orient="records")