from typing import Dict, Any
from ..logic.athlete import Athlete, parse_athlete

class Category:
    def __init__(self, name):
        self.name = name
        self.athletes = []
        self.min_interval = 1
        self.vacants_count = 0
        self.categories_w_same_course = []
        self.first_control = "-1"
        self.course = f'without_course_{name}'
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

    def get_last_athlete_startime(self):
        if self.final_interval == None or self.final_start == None:
            return 0
        else:
            return self.final_start + (self.get_category_count() - 1) * self.final_interval

def parse_category(cat_dict:Dict[str,Any]) -> Category:
    cat = Category(cat_dict['name'])
    cat.athletes = [parse_athlete(athlete_json) for athlete_json in cat_dict['athletes']]
    cat.min_interval = int(cat_dict['min_interval'])
    cat.vacants_count = int(cat_dict['vacants_count'])
    cat.categories_w_same_course = [course for course in cat_dict['categories_w_same_course']]
    cat.first_control = cat_dict['first_control']
    cat.course = cat_dict['course'] if cat_dict['course'] != None else f'withut_course_{cat.name}'
    cat.near_category = [cat for cat in cat_dict['near_category']]
    cat.far_category = [ cat for cat in cat_dict['far_category']]
    cat.final_interval = cat_dict['final_interval']
    cat.final_start = cat_dict['final_start']
    cat.has_interval_start = cat_dict['has_interval_start']
    cat.start = cat_dict['start']
    if int(cat_dict['athletes_count']) > len(cat.athletes):
        add_athletes(cat, cat_dict['athletes_count'] - len(cat.athletes))
    return cat

def add_athletes(cat:Category, count:int) -> None:
    for _ in range(count):
        cat.athletes.append(Athlete('',''))