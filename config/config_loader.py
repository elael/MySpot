from datetime import datetime, date, time, timedelta
from typing import NamedTuple, Dict, Tuple, List, Any

import yaml


class Configuration(NamedTuple):
    hours: Tuple[str]
    kitchens: List[Dict[str, Any]]
    fruit_types: Tuple[str]


def load_config():
    with open('config/config.yaml') as config_file:
        cfg = yaml.safe_load(config_file)

    initial_time = datetime.combine(date.today(), time.fromisoformat(cfg['general']['start_time']))
    final_time = datetime.combine(date.today(), time.fromisoformat(cfg['general']['final_time']))
    dt = timedelta(minutes=cfg['general']['delta_minutes'])
    steps = round((final_time - initial_time) / dt)
    return Configuration(
        hours=tuple((initial_time + n * dt).strftime('%H:%M') for n in range(steps)),
        kitchens=cfg['kitchens'],
        fruit_types=cfg['fruit_types']
    )
