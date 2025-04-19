from src.timetable import convert_date
from src.calculator import get_price

import json
import random


id_counter = 0

trucks = [
    "Грузовик",
    "Фургон",
    "Газель",
    "Цистерна",
    "Тягач с полуприцепом"
]

frequency = [
    "по запросу",
    "раз в неделю",
    "два раза в неделю",
    "каждый день",
    "через день"
]

torg = [True, False]

WEIGHT_MAX = 10000
WEIGHT_MIN = 1000

VOLUME_MAX = 60
VOLUME_MIN = 10


with open("data/companies.json", "r", encoding="UTF-8") as f:
    companies = json.loads(f.read())


class Transfer:
    """
    {
        company: str
        fr: str
        to: str 

        cargo_type: str
        weight: num
        volume: num

        depart: str
    }
    """
    def __init__(self, data):
        global id_counter

        self.fr = data["Откуда"]
        self.to = data["Куда"]

        self.cargo_type = data["Тип груза"]
        self.weight = float(data["Вес груза"])
        self.volume = float(data["Объём груза"])

        self.depart = None

    async def to_dict(self) -> dict:
        global id_counter

        weight = int(self.weight)
        volume = int(self.volume)

        id_counter += 1

        return {
            "ID": id_counter,
            "Название компании": random.choice(companies)["Название"],
            "Вид транспорта": random.choice(trucks),
            "Максимальная грузоподъемность": random.randint(min(WEIGHT_MIN, weight), max(WEIGHT_MAX, weight)),
            "Максимальный вместимый объем": random.randint(min(VOLUME_MIN, volume), max(VOLUME_MAX, volume)),
            "Когда отправляет": random.choice(frequency),
            "Ставка": await get_price(self),
            "Возможность торга": random.choice(torg)
        }

