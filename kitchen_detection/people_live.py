"""
A "live mess" that buffers output from YOLO.
It averages and adds to history after each hour.
"""
import subprocess
from collections import deque
from datetime import timedelta, datetime
from threading import Thread
from time import sleep

import schedule

from config import cfg
from kitchen_database import kitchens_at, Kitchen, kitchens_add_history, MissingDBTimeError
from utils import avg

fruit_buffer = {fruit: deque([0.0], maxlen=10) for fruit in cfg.fruit_types}
people_buffer = deque([0], maxlen=10)


def read_out():
    for line in process.stdout:
        entry, *values = line.split(':')
        if entry == "people":  # Contract with YOLO
            people_buffer.append(int(values[0]))
        if entry in fruit_buffer:
            fruit_buffer[entry].append(float(values[0]))


process = subprocess.Popen("./object_detection_yolo/build/object_detection_yolo", bufsize=0, shell=False,
                           stdout=subprocess.PIPE, universal_newlines=True)
Thread(target=read_out, daemon=True).start()


def history_saver():
    from kitchen_detection.people_counting import LiveInfo
    from statistics import mode

    people = []
    fruits_history = {fruit: [] for fruit in cfg.fruit_types}
    dt = timedelta(minutes=30)

    def saving():
        begin_time = datetime.now() - dt
        round_time = begin_time.replace(minute=30 * (begin_time.minute // 30)).strftime('%H:%M')
        try:
            kits = kitchens_at(round_time)
        except MissingDBTimeError:
            return
        new_kits = []
        for kit in kits:
            if kit.name == 'Cadillac':  # Only Cadillac is live for now, do not update the rest
                dkit = kit._asdict()
                dkit['people'] = avg(people)
                dkit['fruits'] = {fruit: avg(values) for fruit, values in fruits_history.items()}
                new_kits.append(Kitchen(**dkit))
        kitchens_add_history(LiveInfo(round_time, new_kits))
        people.clear()
        for fruit in fruits_history.values():
            fruit.clear()

    schedule.every().minute.at(":30").do(saving)
    while True:
        people.append(mode(people_buffer))
        for fruit, history in fruits_history.items():
            history.append(avg(fruit_buffer[fruit]))
        schedule.run_pending()
        sleep(60)


Thread(target=history_saver, daemon=True).start()
