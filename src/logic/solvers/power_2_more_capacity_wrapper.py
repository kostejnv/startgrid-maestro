import copy

from ..solvers.solver import Solver
from ..categories_modificators.courses_joiner_low import CoursesJoinerLow
import copy
import random

def get_category_count_for(list_of_cats):
    return sum([cat.get_category_count() for cat in list_of_cats])

def group_cats_based_on_resource(categories):
    resources = {}
    for cat in categories:
        if cat.first_control in resources:
            resources[cat.first_control].append(cat)
        else:
            resources[cat.first_control] = [cat]
    return list(resources.values())

def to_dict(cats_list):
    return {cat.name:cat for cat in cats_list}


def partition_cats(resources_list, capacity):
    partitions = [[] for _ in range(capacity)]
    for resourcse_cats in resources_list:
        part_with_min_count = partitions.index(min(partitions, key=lambda part: sum([get_category_count_for(resource) for resource in part])))
        partitions[part_with_min_count].append(resourcse_cats)
    partitions = [[cat for resource in part for cat in resource] for part in partitions] # flatten parts
    return partitions


class Power2SolverMoreCapacityWrapper(Solver):
    def __init__(self, solver, joiner):
        self.solver = solver
        self.joiner = joiner

    def solve(self, event):
        event = copy.deepcopy(event)
        categories = event.get_not_empty_categories_with_interval_start()
        categories =  self.joiner.join(list(categories.values()))

        resources_list = group_cats_based_on_resource(categories.values())  # resoursec_list is list of lists of categories
        min_schedule_length = get_category_count_for(categories.values()) * max(
            [cat.min_interval for cat in categories.values()]) * len(
            categories)  # upper bound for schedule
        best_cats = {}
        for _ in range(50):
            random.shuffle(resources_list)
            cats_for_separete_machine = partition_cats(resources_list, event.capacity)
            solved_cats = []
            max_schedule_length = 0
            for cats_for_machine in cats_for_separete_machine:
                event.categories = to_dict(cats_for_machine)
                solved_cats_for_one_maschine, schedule_length = self.solver.solve(copy.deepcopy(event))
                solved_cats.append(solved_cats_for_one_maschine)
                max_schedule_length = max(max_schedule_length, schedule_length)

            if max_schedule_length < min_schedule_length:
                best_cats = {key:val for dic in solved_cats for key,val in dic.items()}
                min_schedule_length = max_schedule_length

        return self.joiner.disjoin(list(best_cats.values())), min_schedule_length

    def get_name(self):
        return f'{self.solver.get_name()}'
