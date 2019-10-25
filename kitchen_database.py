import json
from datetime import time, datetime, date, timedelta
from typing import NamedTuple, Tuple, TypedDict, Dict


class MissingDBTimeError(ValueError):
    """Should be used when requested time is not present on the database"""


# Time range configuration
initial_time = datetime.combine(date.today(), time(hour=10, minute=0))
final_time = datetime.combine(date.today(), time(hour=17, minute=0))
dt = timedelta(minutes=30)
steps = int((final_time - initial_time) / dt)
hours = [(initial_time + n * dt).strftime('%H:%M') for n in range(steps)]

KITCHEN_SEATS = {'Cadillac': 6, 'Pit Stop': 13, 'Delorean': 8, 'Jeep': 19}
FRUIT_TYPES = ['banana', 'pear', 'peach', 'grape', 'orange', 'apple']


class Kitchen(NamedTuple):
    name: str
    seats: int
    people: int
    fruits: Dict[str, int]

    @property
    def empty_seats(self):
        return max(self.seats - self.people, 0)


def kitchens_at(time_frame: str) -> Tuple[Kitchen]:
    hour = time.fromisoformat(time_frame).strftime('%H:%M')
    with open('kitchen_history.json', 'r') as fp:
        history = json.load(fp)

        if hour not in history:
            raise MissingDBTimeError(f"Time {hour} is not present in the database.")

        return tuple(Kitchen(**kitchen) for kitchen in history[hour])
