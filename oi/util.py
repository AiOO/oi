import time

TIME_SECONDS = 1000
TIME_MINUTES = TIME_SECONDS * 60
TIME_HOURS = TIME_MINUTES * 60
TIME_DAYS = TIME_HOURS * 24

def timestamp():
    return int(round(time.time() * 1000))

