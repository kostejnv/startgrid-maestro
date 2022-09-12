from collections import Counter


class Courses_manager:
    def __init__(self, courses_str: str):
        courses_str = courses_str.split("\n")
        self.courses = [line.replace('\n', '').split('\t') for line in courses_str][1:] # parse file format

    def add_courses_info_to_cats(self, event) -> None:
        cats = event.categories
        course_idx = 1
        courses_orders = {}
        for course in self.courses:
            act_category_name = course[0]
            act_controls_order = course[-1]
            if act_category_name in cats: # check this course has category in system
                if act_controls_order not in courses_orders: #create new course name
                    courses_orders[act_controls_order] = str(course_idx)
                    course_idx += 1
                cats[act_category_name].course = courses_orders[act_controls_order] # add course to category
                cats[act_category_name].first_control = act_controls_order.split('-')[1]
                cats[act_category_name].categories_w_same_course = \
                    [cat[0] for cat in self.courses if (cat[-1] == act_controls_order) & (cat[0] != act_category_name)]
            else:
                print(f'WARNING: Category {act_category_name} has course but it is not registered in system') #TODO

        #check if we have all courses
        for cat_name in cats:
            if cat_name not in [course[0] for course in self.courses]:
                print(f"WARNING: There is no course for category '{cat_name}'") #TODO
