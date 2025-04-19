from fastapi import FastAPI
from src.distance import calculate_distance
from data.spec import specification, BASE_URL

import uvicorn
import asyncio


app = FastAPI()

@app.get("/")
def root_func():
    distance = asyncio.run(calculate_distance("Paris", "Berlin"))
    return f"Logistic API {specification["id"]}", 200


    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
