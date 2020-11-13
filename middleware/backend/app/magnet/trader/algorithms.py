from typing import Callable
from magnet.vendors import MiniDB


class DetectorRepository(MiniDB[Callable]):
    pass


detectors = DetectorRepository()


@detectors.add
def detect_t_cross(ticker):
    # サイン検出
    if ticker.t_cross == 0:
        return None
    elif ticker.t_cross == 1:
        return "ask"
    elif ticker.t_cross == -1:
        return "bid"
    else:
        raise Exception()


@detectors.add
def detect_t_cross_invert(ticker):
    # サイン検出
    if ticker.t_cross == 0:
        return None
    elif ticker.t_cross == -1:
        return "ask"
    elif ticker.t_cross == 1:
        return "bid"
    else:
        raise Exception()

