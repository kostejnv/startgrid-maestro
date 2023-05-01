from ..category import Category
from ..event import Event
from math import ceil,log2

def set_all_intervals_same(cats):
    max_interval = max([cat.min_interval for cat in cats.values()])
    for cat in cats.values():
        cat.min_interval = max_interval
    return max_interval, cats

def set_all_intervals_to_power_2(cats):
    for cat in cats.values():
        cat.min_interval = 2**(ceil(log2(cat.min_interval)))
    return cats