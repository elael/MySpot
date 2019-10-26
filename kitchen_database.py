import json
from datetime import time
from typing import NamedTuple, Tuple, Dict


class MissingDBTimeError(ValueError):
    """Should be used when requested time is not present on the database"""


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
