from src.logic.categories_modificators.courses_joiner_low import CoursesJoinerLow
from src.logic.solvers.solver import Solver


def first_possible_minute(cat, schedule, capacity):
    for minute, controls in enumerate(schedule):
        if len(controls) < capacity and cat.first_control not in controls:
            return minute


class GreedyLongFirstSolver(Solver):
    def __init__(self, joiner):
        self.joiner = joiner

    def solve(self, event):
        categories = event.get_not_empty_categories_with_interval_start()
        categories =  self.joiner.join(list(categories.values()))
        interval = max([cat.min_interval for cat in categories.values()])
        # initialisation
        opt_upper_bound = sum([cat.min_interval * cat.get_category_count() for cat in categories.values()])
        res = [[] for _ in range(opt_upper_bound)]
        for cat in categories.values():
            cat.final_interval = interval
        sorted_cats = sorted(categories.values(), key=lambda cat: cat.get_category_count(), reverse=True)
        for cat in sorted_cats:
            cat.final_start = first_possible_minute(cat, res, event.capacity)
            for j in range(cat.get_category_count()):
                idx = cat.final_start + j * interval
                res[idx].append(cat.first_control)
        c_max = max([i + 1 for i in range(len(res)) if res[i]])
        return self.joiner.disjoin(list(categories.values())), c_max

    def get_name(self):
        return 'GreedyLength'
