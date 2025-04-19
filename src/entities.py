from src.calculator import get_price
from src.timetable import convert_date, reconvert_date, increase_date

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

DELIVER_MAX = 10
DELIVER_MIN = 1

def get_phone():
    number = "+7"
    for _ in range(10):
        number += str(random.randint(0, 10))

    return number


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

        self.depart = convert_date(int(data["Дата отправки"]) / 1000)

    async def to_dict(self) -> dict:
        global id_counter

        weight = int(self.weight)
        volume = int(self.volume)

        id_counter += 1

        company = random.choice(companies)

        return {
            "ID результата": id_counter,
            "Вид транспорта": random.choice(trucks),
            "Макс. грузоподъемность": random.randint(min(WEIGHT_MIN, weight), max(WEIGHT_MAX, weight)),
            "Макс. объём кузова": random.randint(min(VOLUME_MIN, volume), max(VOLUME_MAX, volume)),
            "Когда отправляет": random.choice(frequency),
            "Ставка": await get_price(self),
            "Возможность торга": random.choice(torg),
            "Дата погрузки": reconvert_date(self.depart) * 1000,
            "Дата доставки": reconvert_date(increase_date(self.depart, random.randint(DELIVER_MIN, DELIVER_MAX))) * 1000,
            
            "Название компании": company["Название"],
            "Контактный телефон": company["Контакты"],
            "ИНН": company["ИНН"],
            "Сайт компании": company["Сайт"],
            "Юридический адрес": company["Юридический адрес"]
        }

