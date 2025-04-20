from fastapi import FastAPI, Request
from data.spec import specification
from src.entities import Transfer
from random import randint

import uvicorn
import sys


app = FastAPI()

PORT = 3000

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

@app.post("/ack")
async def ack_choice(req: Request):
    return {"status": "Approved"}
    

if __name__ == "__main__":
    if len(sys.argv) == 3:
        specification["id"] = int(sys.argv[1])
        specification["km_price"] = int(sys.argv[2])
    else:
        print(f"Invalid number of args {len(sys.argv)}")
        exit(1) 

    uvicorn.run(app, host="0.0.0.0", port=PORT)
