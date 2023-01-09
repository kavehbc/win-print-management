import datetime


def get_date_time_delta(first_datetime, second_datetime=datetime.datetime.now()):
    seconds_diff = (second_datetime - first_datetime).seconds
    minutes_diff = int(seconds_diff / 60)
    return minutes_diff
