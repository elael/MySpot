from datetime import datetime, timedelta
from random import randint, random
from statistics import mode
from typing import Iterator, NamedTuple

from config import cfg
from kitchen_database import Kitchen
import kitchen_detection.people_live
from utils import avg


class LiveInfo(NamedTuple):
    time: str
    kitchens: Iterator[Kitchen]

    def recursive_dict(self) -> dict:
        rec_dict = self._asdict()
        rec_dict['kitchens'] = list(kitchen._asdict() for kitchen in self.kitchens)
        return rec_dict

    def with_boolean_fruits(self):
        return LiveInfo(self.time, (kitchen.round() for kitchen in self.kitchens))


def get_current() -> LiveInfo:
    kitchens = []
    for kitchen in cfg.kitchens:
        if kitchen['name'] == 'Cadillac':  # Only Cadillac is live now, fake the rest
            people = mode(kitchen_detection.people_live.people_buffer)
            fruits = {fruit: avg(history) for fruit, history in kitchen_detection.people_live.fruit_buffer.items()}
        else:
            people = kitchen['seats']/2
            fruits = {'apple': 1}

        kitchens.append(Kitchen(kitchen['name'],
                                kitchen['seats'],
                                kitchen['floor'],
                                people,
                                fruits))

    begin_time = datetime.now()
    round_time = begin_time.replace(minute=30 * (begin_time.minute // 30)).strftime('%H:%M')
    return LiveInfo(round_time, kitchens)
