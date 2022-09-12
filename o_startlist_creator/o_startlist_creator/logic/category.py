import json
from o_startlist_creator.logic.athlete import Athlete, parse_athlete

class Category:
    def __init__(self, name):
        self.name = name
        self.athletes = []
        self.min_interval = 1
        self.vacants_count = 0
        self.categories_w_same_course = []
        self.first_control = "-1"
        self.course = None
        self.near_category = []
        self.far_category = []
        self.final_interval = None
        self.final_start = None
        self.has_interval_start = True
        self.start = 'S1'

    def get_category_count(self):
        return len(self.athletes) + self.vacants_count

    def to_dict(self):
        category_dict = self.__dict__
        category_dict['athletes'] = [athlete.__dict__ for athlete in category_dict['athletes']]
        category_dict['athletes_count'] = len(category_dict['athletes'])
        return category_dict

def parse_category(cat_json:json) -> Category:
    cat = Category(cat_json.name)
    cat.athletes = [parse_athlete(athlete_json) for athlete_json in cat_json.athletes]
    cat.min_interval = int(cat_json.min_interval)
    cat.vacants_count = int(cat_json.vacants_count)
    cat.categories_w_same_course = [course for course in cat_json.categories_w_same_course]
    cat.first_control = cat_json.first_control
    cat.course = cat_json.course
    cat.near_category = [cat for cat in cat_json.near_category]
    cat.far_category = [ cat for cat in cat_json.far_category]
    cat.final_interval = cat_json.final_interval
    cat.final_start = cat_json.final_start
    cat.has_interval_start = cat_json.has_interval_start
    cat.start = cat_json.start
    if int(cat_json.athletes_count) > len(cat.athletes):
        add_athletes(cat, cat_json.athletes_count - len(cat.athletes))
    return cat

def add_athletes(cat:Category, count:int) -> None:
    for _ in range(count):
        cat.athletes.append(Athlete('',''))