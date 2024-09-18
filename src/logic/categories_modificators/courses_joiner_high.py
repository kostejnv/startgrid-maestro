from ...entities.category import Category
from ..categories_modificators.utils import to_dict, set_all_intervals_to_power_2
from copy import deepcopy


class CoursesJoinerHigh:
    def __init__(self):
        self.was_joined = False
        self.original_cats = None
        self.cats_of_course = {}

    def get_name(self):
        return "-HighInt"

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
        self.__save_cats_of_courses(course_name, cats_to_join)  # remeber the cats of give courses for disjoin
        joined_cat = Category(course_name)
        joined_cat.course = course_name
        joined_cat.first_control = cats_to_join[0].first_control
        joined_cat.vacants_count = sum([cat.get_category_count() for cat in cats_to_join])
        joined_cat.min_interval = max([cat.min_interval for cat in cats_to_join])

        return joined_cat

    def __disjoin_joined_cat(self, solved_course: Category) -> list:
        rest_of_solved_course = deepcopy(solved_course)
        cats = self.__get_cats_of_course(solved_course.name)
        solved_cats = []
        for cat in cats:
            solved_cat = self.__pop_cat_from_course(rest_of_solved_course, cat)
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

    def __get_cats_of_course(self, cat_name: str) -> list:
        return self.cats_of_course[cat_name]

    def __pop_cat_from_course(self, rest_of_solved_course: Category, cat_to_pop: Category) -> Category:
        '''
        cat_to_pop is always in the begining of the rest_of_solved_courses
        '''
        poped_cat = deepcopy(cat_to_pop)
        poped_cat.final_interval = rest_of_solved_course.final_interval
        poped_cat.final_start = rest_of_solved_course.final_start

        # change final_start in rest_of_solved_courses
        rest_of_solved_course.final_start += rest_of_solved_course.final_interval * poped_cat.get_category_count()

        return poped_cat

    def __transfer_data_to_single_original_cat(self, org_cat: Category, new_cat: Category) -> None:
        org_cat.final_interval = new_cat.final_interval
        org_cat.final_start = new_cat.final_start