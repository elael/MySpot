import json
from typing import NamedTuple, Tuple, Dict


class MissingDBTimeError(ValueError):
    """Should be used when requested time is not present on the database"""


class Kitchen(NamedTuple):
    name: str
    seats: int
    floor: int
    people: int
    fruits: Dict[str, int]

    @property
    def empty_seats(self):
        return max(self.seats - self.people, 0)

    def round(self) -> 'Kitchen':
        return Kitchen(self.name, self.seats, self.floor, round(self.people),
                       {fruit: round(change) for fruit, change in self.fruits.items()})


def kitchens_at(hour: str) -> Tuple[Kitchen]:
    with open('kitchen_history.json', 'r') as fp:
        history = json.load(fp)

        if hour not in history:
            raise MissingDBTimeError(f"Time {hour} is not present in the database.")

        return tuple(Kitchen(**kitchen) for kitchen in history[hour])


def kitchens_add_history(new_info: 'LiveInfo'):
    """
    Add a new info to the history.
    History is update using an exponential decaying weighted average.
    :param new_info: contains information about the kitchens and time of the new information.
    """
    with open('kitchen_history.json', 'r') as fp:
        history = json.load(fp)

    for kit in new_info.kitchens:  # TODO smarter way to match pairs
        for n, hkit in enumerate(history[new_info.time]):
            if hkit['name'] == kit.name:
                break
        else:
            continue  # continue if no match is found
        history[new_info.time][n]['people'] *= 0.9
        history[new_info.time][n]['people'] += 0.1 * kit.people
        for fruit, value in history[new_info.time][n]['fruits'].items():
            history[new_info.time][n]['fruits'][fruit] = 0.9*value + 0.1*kit.fruits.get(fruit, value)

    with open('kitchen_history.json', 'w') as fp:
        json.dump(history, fp, indent=2)


def save_random_db():
    """For fake demonstration"""
    from kitchen_detection.people_counting import get_current
    from config import cfg
    with open('kitchen_history.json', 'w') as fp:
        json.dump({hour: get_current().recursive_dict()['kitchens'] for hour in cfg.hours}, fp, indent=2)
