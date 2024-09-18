from src.logic.solvers.solver import Solver


class LowerBoundSolver(Solver):
    '''
    This is not solver! It makes lower bound of the problem
    '''

    def __init__(self):
        pass

    def solve(self, event):
        categories = event.get_not_empty_categories_with_interval_start()

        density_bound = self.__get_density_bound(categories.values(), event.capacity)
        one_resource_bound = self.__get_most_common_1st_control_athetes_count(categories.values())
        largest_cat_bound = self.__get_longest_category_length(categories.values())

        final_lower_bound = max(density_bound, one_resource_bound, largest_cat_bound)
        return categories, final_lower_bound

    def get_name(self):
        return 'LowerBoundSolver'

    def __get_density_bound(self, cats, capacity):
        athletes_count = sum([cat.get_category_count() for cat in cats])
        return athletes_count//capacity

    def __get_most_common_1st_control_athetes_count(self, cats):
        controls = set()
        for cat in cats:
            controls.add(cat.first_control)

        max_athlets_count = 0
        for control in controls:
            athetes_count = sum([cat.get_category_count() for cat in cats if cat.first_control == control])
            max_athlets_count = max(max_athlets_count,athetes_count)
        return max_athlets_count


    def __get_longest_category_length(self, cats):
        cats_lengths = [(cat.get_category_count()-1) * cat.min_interval + 1 for cat in cats]
        return max(cats_lengths)