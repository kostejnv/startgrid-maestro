from o_startlist_creator.logic.categories_modificators.courses_joiner_low import CoursesJoinerLow
from o_startlist_creator.logic.solvers.solver import Solver


def first_possible_minute(cat, schedule, capacity):
    for minute, controls in enumerate(schedule):
        if len(controls) < capacity and cat.first_control not in controls:
            return minute


def get_most_frequent_resource(cats):
    res = {}
    for cat in cats: res[cat.first_control] = 0
    for cat in cats: res[cat.first_control] += cat.get_category_count()
    return max(res.items(), key=lambda r: r[1])[0]


class GreedyByResouresSolver(Solver):
    def __init__(self, joiner):
        self.joiner = joiner
        pass

    def solve(self, event):
        categories = event.get_not_empty_categories_with_interval_start()
        categories =  self.joiner.join(list(categories.values()))
        interval = max([cat.min_interval for cat in categories.values()])
        # initialisation
        unused_cats = list(categories.values())
        opt_upper_bound = sum([cat.min_interval * cat.get_category_count() for cat in categories.values()])
        res = [[] for _ in range(opt_upper_bound)]
        for cat in categories.values():
            cat.final_interval = interval
        while unused_cats:
            mfr = get_most_frequent_resource(unused_cats)
            cat = max([cat for cat in unused_cats if (cat.first_control == mfr)], key=lambda cat: cat.get_category_count())
            cat.final_start = first_possible_minute(cat, res, event.capacity)
            for j in range(cat.get_category_count()):
                idx = cat.final_start + j * interval
                res[idx].append(cat.first_control)
            unused_cats.remove(cat)
        c_max = max([i+1 for i in range(len(res)) if res[i]])
        return self.joiner.disjoin(list(categories.values())), c_max

    def get_name(self):
        return 'GreedyRes'