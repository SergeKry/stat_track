import random
import datetime
from datetime import timezone


class Puzzle:
    def __init__(self):
        self.a = random.randint(1, 10)
        self.b = random.randint(1, 10)


def convert_timestamp_from_json(timestamp: str):
    if not timestamp:
        return datetime.datetime.now(timezone.utc)
    timestamp_naive = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp_aware = timestamp_naive.replace(tzinfo=datetime.timezone.utc)
    return timestamp_aware
