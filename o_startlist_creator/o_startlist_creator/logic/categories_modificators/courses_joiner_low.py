from ..category import Category
from ..categories_modificators.utils import to_dict, set_all_intervals_to_power_2
from copy import deepcopy


class CoursesJoinerLow:
    def __init__(self):
        self.was_joined = False
        self.original_cats = None
        self.ratios = {}
        self.cats_of_course = {}

    def get_name(self):
        return "-LowInt"

    def join(self, categories_to_join: list) -> dict:
        self.original_cats = categories_to_join
        cats = set_all_intervals_to_power_2(deepcopy(self.original_cats))
        course_names = set([cat.course for cat in cats])
        joined_cats = []
        for course in course_names:
            cats_w_given_course = [cat for cat in cats if cat.course == course]
            joined_cats.append(self.__built_joined_cat_from(course, cats_w_given_course))
        return to_dict(joined_cats)

    def disjoin(self, solved_joined_categories: list) -> dict:
        solved_cats = []
        for solved_course in solved_joined_categories:
            solved_cats += self.__disjoin_joined_cat(solved_course)
        self.__transfer_data_to_original_cats(solved_cats, self.original_cats)
        return to_dict(self.original_cats)

    def __built_joined_cat_from(self, course_name: str, cats_to_join: list) -> Category:
        sorted_cats = list(sorted(cats_to_join, key=lambda cat: cat.min_interval))
        self.__save_cats_of_courses(course_name, sorted_cats)  # remeber the cats of give courses for disjoin

        joined_cat = self.__construct_initial_cat(sorted_cats[0])
        self.__add_cats_ratios(sorted_cats)  # remember ratios between min cat and given cat interval
        for cat in sorted_cats[1:]:
            self.__add_cat_to_joined_cat(joined_cat, cat)
        return joined_cat

    def __disjoin_joined_cat(self, solved_course: Category) -> list:
        rest_of_solved_course = deepcopy(solved_course)
        cats = self.__get_cats_of_course(solved_course.name)
        solved_cats = []
        for idx, cat in enumerate(cats):
            solved_cat = self.__pop_cat_from_course(rest_of_solved_course, cat, is_first=(idx == 0))
            solved_cats.append(solved_cat)
        return solved_cats

    def __transfer_data_to_original_cats(self, new_cats: list, original_cats: list) -> None:
        new_cats_dict = to_dict(new_cats)
        for org_cat in original_cats:
            if org_cat.name in new_cats_dict:
                self.__transfer_data_to_single_original_cat(org_cat, new_cats_dict[org_cat.name])
            else:
                raise f"category {org_cat.name} is not between solved_categories"

    def __save_cats_of_courses(self, course_name: str, sorted_cats: list) -> None:
        self.cats_of_course[course_name] = sorted_cats

    def __construct_initial_cat(self, first_cat: Category) -> Category:
        init_cat = Category(first_cat.course)

        # add general data
        init_cat.course = first_cat.course
        init_cat.first_control = first_cat.first_control
        init_cat.vacants_count = first_cat.get_category_count()  # number of athletes in first cat
        init_cat.min_interval = first_cat.min_interval  # it is min interval of all categories of this course
        return init_cat

    def __add_cats_ratios(self, sorted_cats: list) -> None:
        min_interval = min([cat.min_interval for cat in sorted_cats])
        for cat in sorted_cats:
            self.ratios[cat.name] = cat.min_interval // min_interval

    def __add_cat_to_joined_cat(self, joined_cat: Category, cat: Category) -> None:
        joined_cat.vacants_count += self.ratios[cat.name] * cat.get_category_count()

    def __get_cats_of_course(self, cat_name: str) -> list:
        return self.cats_of_course[cat_name]

    def __pop_cat_from_course(self, rest_of_solved_course: Category, cat_to_pop: Category, is_first: bool) -> Category:
        '''
        cat_to_pop is always in the begining of the rest_of_solved_courses
        '''
        poped_cat = deepcopy(cat_to_pop)

        poped_cat.final_interval = self.ratios[poped_cat.name] * rest_of_solved_course.final_interval
        if not is_first: #move final start one interval further
            rest_of_solved_course.final_start += poped_cat.final_interval

        poped_cat.final_start = rest_of_solved_course.final_start

        # change final_start in rest_of_solved_courses
        rest_of_solved_course.final_start += (
                                             poped_cat.get_category_count() - 1) * poped_cat.final_interval

        return poped_cat

    def __transfer_data_to_single_original_cat(self, org_cat: Category, new_cat: Category) -> None:
        org_cat.final_interval = new_cat.final_interval
        org_cat.final_start = new_cat.final_start