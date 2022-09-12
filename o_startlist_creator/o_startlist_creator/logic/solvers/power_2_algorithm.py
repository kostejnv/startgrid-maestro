from o_startlist_creator.logic.categories_modificators.courses_joiner_low import CoursesJoinerLow
from o_startlist_creator.logic.solvers.solver import Solver
from o_startlist_creator.logic.solvers.solver_utils import set_all_intervals_to_power_2
from math import floor, log2


def greedy_schedule(cats, max_bin_size):
    bins = []
    for cat in cats:
        was_cat_schedule = False
        for bin in bins:
            bin_size = sum([bin_cat.get_category_count() for bin_cat in bin])
            if max_bin_size >= bin_size + cat.get_category_count():
                bin.append(cat)
                was_cat_schedule = True
                break
        if not was_cat_schedule:
            bins.append([cat])
    return bins


def schedule_bin(cats, G, con):
    bin_time = 0
    for c in cats:
        c.final_interval = G
        c.final_start = bin_time * G + con
        bin_time += c.get_category_count()


def greedy_schedule_improved(cats, max_bin_size):
    bins = []
    cats = list(sorted(cats,key=lambda cat: cat.get_category_count(), reverse=True))
    for cat in cats:
        was_cat_schedule = False
        for bin in bins:
            bin_size = sum([bin_cat.get_category_count() for bin_cat in bin])
            if max_bin_size/2 > bin_size:
                bin.append(cat)
                was_cat_schedule = True
                break
        if not was_cat_schedule:
            bins.append([cat])
    return bins


class Power2Solver(Solver):
    def __init__(self, joiner, improved=False):
        self.improved = improved
        self.joiner = joiner



    def solve(self, event):
        S = event.get_not_empty_categories_with_interval_start()
        S = set_all_intervals_to_power_2(S)
        S =  self.joiner.join(list(S.values()))
        S, length = self.algorithm(S)
        return self.joiner.disjoin(list(S.values())), length

    def algorithm(self, S):
        if not S:
            return S, 0
        b1 = max([(c.get_category_count() - 1) * c.min_interval + 1 for c in S.values()])
        b2 = sum([c.get_category_count() for c in S.values()])
        t = max(b1, b2)
        max_interval = max([c.min_interval for c in S.values()])
        PC = {}
        for i in range(int(log2(max_interval))):
            PC[2**i] = []
        for c in S.values():
            if c.min_interval in PC:
                PC[c.min_interval].append(c)
            else:
                PC[c.min_interval] = [c]
        CC = [0]
        G = 1
        unused_cats = list(S.values())
        while unused_cats:
            bins = greedy_schedule(PC[G], floor(2 * t / G)) if not self.improved else greedy_schedule_improved(PC[G], floor(2 * t / G))
            for bin in bins:
                if sum([c.get_category_count() for c in bin]) >= t / G:
                    i = CC.pop(0)
                    schedule_bin(bin, G, i)
                    for c in bin:
                        unused_cats.remove(c)
                else:
                    if 2 * G not in PC:
                        PC[2 * G] = []
                    PC[2 * G] = PC[2 * G] + bin
            CC = CC + [G + i for i in CC]
            G = 2 * G
        c_max = max([(c.get_category_count() - 1) * c.final_interval + 1 + c.final_start for c in S.values()])
        return S, c_max




    def get_name(self):
        return f'Doubling{self.joiner.get_name()}-Full' if not self.improved else f'Doubling{self.joiner.get_name()}-Half'