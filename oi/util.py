import random
import time

TIME_SECONDS = 1000
TIME_MINUTES = TIME_SECONDS * 60
TIME_HOURS = TIME_MINUTES * 60
TIME_DAYS = TIME_HOURS * 24

def timestamp():
    return int(round(time.time() * 1000))

def get_random_string(length):
    return ''.join(chr(random.choice(range(127))) for _ in range(length))

