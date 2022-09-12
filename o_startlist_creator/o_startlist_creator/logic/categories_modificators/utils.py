from math import ceil,log2

def set_all_intervals_same(cats):
    max_interval = max([cat.min_interval for cat in cats.values()])
    for cat in cats.values():
        cat.min_interval = max_interval
    return max_interval, cats

def set_all_intervals_to_power_2(cats):
    if type(cats) is dict:
        for cat in cats.values():
            cat.min_interval = 2**(ceil(log2(cat.min_interval)))
    elif type(cats) is list:
        for cat in cats:
            cat.min_interval = 2**(ceil(log2(cat.min_interval)))
    else:
        raise "no list no dict"
    return cats


def to_dict(categories: list) -> dict:
    return {cat.name:cat for cat in categories}