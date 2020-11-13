from typing import Union, Literal
import datetime


def create_schedule(before, until):
    if before > until:
        raise Exception()

    diff = (until - before).days
    start_day = datetime.date.today() - datetime.timedelta(days=diff)
    for day_count in range(diff):
        yield start_day + datetime.timedelta(days=day_count)


def create_stream(scheuler):
    pass


def run_by_stop_and_reverse():
    """ドテン方式トレード"""
    pass


def detect_signal(self, ticker) -> Union[Literal["ask", "bid"], None]:
    # サイン検出
    if ticker.t_cross == 0:
        return None
    elif ticker.t_cross == 1:
        return "ask"
    elif ticker.t_cross == -1:
        return "bid"
    else:
        raise Exception()
