from fastapi import FastAPI, Request
from src.distance import calculate_distance
from data.spec import specification, BASE_URL
from src.entities import Transfer
from src.timetable import is_delivery_day
from random import randint

import uvicorn
import asyncio


app = FastAPI()

MAX_BATCH = 10
MIN_BATCH = 3

@app.get("/")
def root_func():
    return f"Logistic API {specification["id"]}"


@app.post("/search")
async def search_transfers(req: Request):
    try:
        transfer = Transfer(await req.json())

        batch = randint(MIN_BATCH, MAX_BATCH)
        transfers = [await transfer.to_dict() for _ in range(batch)]

        return transfers
    except Exception as e:
        print(f"Error: {e}")
        return None

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
