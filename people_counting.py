from datetime import datetime
from random import randint, random
from typing import Iterator, NamedTuple

from config import cfg
from kitchen_database import Kitchen


class LiveInfo(NamedTuple):
    time: str
    kitchens: Iterator[Kitchen]

    def recursive_dict(self) -> dict:
        rec_dict = self._asdict()
        print(self.kitchens)
        rec_dict['kitchens'] = list(kitchen._asdict() for kitchen in self.kitchens)
        return rec_dict


def get_current() -> LiveInfo:
    return LiveInfo(datetime.now().time().replace(minute=30).strftime('%H:%M'),
                    [Kitchen(name, seats, randint(0, seats), {fruit: random() for fruit in cfg.fruit_types})
                     for name, seats in cfg.kitchen_seats.items()])
