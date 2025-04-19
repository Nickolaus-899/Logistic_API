from data.spec import specification
from src.distance import calculate_distance
from random import randint


ADEQUATE_COEFF = 2.0

MAX_W = 70
MIN_W = 10

MAX_V = 70
MIN_V = 10

async def get_price(transfer):
    dist_res = await calculate_distance(transfer.fr, transfer.to)
    distance = -1
    if "result" in dist_res.keys():
        distance = dist_res["result"]
    else:
        if "error" in dist_res.keys():
            print("Error: ", dist_res["error"])
        return -1
    price_dist = distance * specification["km_price"]
    
    weight_k = randint(MIN_W, MAX_W)
    volume_k = randint(MIN_V, MAX_V)

    price_cargo = transfer.weight * weight_k + transfer.volume * volume_k

    return (price_dist + price_cargo) * ADEQUATE_COEFF