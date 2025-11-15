# helpers.py
# MZ/X – Általános segédfüggvények

import numpy as np

def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default


def percent_change(old, new):
    if old is None or new is None:
        return 0
    try:
        return (new - old) / old
    except ZeroDivisionError:
        return 0


def normalize(value, min_val, max_val):
    if max_val - min_val == 0:
        return 0
    return (value - min_val) / (max_val - min_val)


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def avg(values):
    if not values:
        return 0
    return sum(values) / len(values)


def trend_direction(value):
    """
    -1 = erős csökkenés
     0 = oldalazás
     1 = enyhe emelkedés
     2 = erős emelkedés
    """
    if value < -0.01:
        return -1
    elif -0.01 <= value <= 0.01:
        return 0
    elif 0.01 < value <= 0.03:
        return 1
    else:
        return 2


def volatility_score(vol):
    """
    Egyszerű vol alapú AI értékelés.
    """
    if vol < 0.005:
        return 0  # alacsony vol
    elif vol < 0.02:
        return 1  # normál vol
    else:
        return 2  # magas vol
