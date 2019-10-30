from typing import Collection


def avg(seq: Collection):
    if len(seq) == 0:
        return 0
    return sum(seq) / len(seq)
