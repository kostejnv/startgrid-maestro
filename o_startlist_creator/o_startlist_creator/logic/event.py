

import csv
import json
from o_startlist_creator.logic.oris_import import *
from o_startlist_creator.logic.category import Category, parse_category

from o_startlist_creator.logic.input_manager.classes_manager import Classes_manager
from o_startlist_creator.logic.input_manager.entries_manager import Entries_manager
from o_startlist_creator.logic.input_manager.event_manager import Event_manager
from o_startlist_creator.logic.input_manager.constraints_manager import ConstrainsManager
from o_startlist_creator.logic.input_manager.courses_manager import Courses_manager
from o_startlist_creator.logic.categories_modificators.utils import to_dict


class Event:
    def __init__(self) -> None:
        self.id = None
        self.name = None
        self.organizator = None
        self.region = None
        self.discipline = None
        self.capacity = None
        self.date = None
        self.categories = {}
        self.solved = False
        self.has_data = False

    def add_dat_from_oris(self, oris_id:int) -> None:
        event_json = download_classes(oris_id)
        entries_json = download_entries(oris_id)

        self.__add_general_info(event_json)
        self.__add_classes_info(event_json)
        self.__add_athletes(entries_json)
        ConstrainsManager().add_constraints_to_cats(self)

        self.has_data = True

    def DEBUG_add_dat_from_oris(self, event_json:json, entries_json:json) -> None:
        self.__add_general_info(event_json)
        self.__add_classes_info(event_json)
        self.__add_athletes(entries_json)
        ConstrainsManager().add_constraints_to_cats(self)

        self.has_data = True

    def get_not_empty_categories_with_interval_start(self):
        return {name: category for name, category in self.categories.items() if
                category.has_interval_start and category.get_category_count() > 0}

    

    def add_data_from_courses_file(self, file_str: str) -> None:
        Courses_manager(file_str).add_courses_info_to_cats(self)

    def export_input_data_to_dict(self) -> json:
        if not self.has_data:
            raise "ERROR: No data imported"
        event_dict = self.__dict__
        event_dict['categories'] = [cat.to_dict() for cat in event_dict['categories'].values()]
        return event_dict
    
    def export_final_data_to_csv(self) -> csv:
        if not self.solved:
            raise "ERROR: Event has not been solved yet"
        data = ['Kategorie, START, INTERVAL, Pocet zavodniku, Int. start, Min. interval, Pocet vakantu, Trat, 1. kontrola'] + [
            f'{cat.name}, {cat.final_start}, {cat.final_interval}, {cat.get_category_count()}, {cat.has_interval_start}, {cat.min_interval}, {cat.vacants_count}, {cat.course}, {cat.first_control}' for cat in self.categories.values()]
        return '\n'.join(data)
        

    def add_results(self) -> None:
        pass

        self.solved = True

    #___________________________________________________
    # private methods

    def __add_general_info(self, event_json:json) -> None:
        Event_manager().add_info(self,event_json)

    def __add_classes_info(self, event_json:json) -> None:
        self.categories = Classes_manager().get_categories(event_json)

    def __add_athletes(self, entries_json:json) -> None:
        Entries_manager().add_athletes_info_to_cats(self, entries_json)

def parse_event(event_json:json) -> Event:
    event = Event()
    event.id = int(event_json.id)
    event.name = event_json.name
    event.organizator = event_json.organizator
    event.region = event_json.region
    event.discipline = event_json.discipline
    event.capacity = 5
    event.date = event_json.date
    event.solved = False
    event.has_data = True
    event.categories = to_dict([parse_category(cat_json) for cat_json in event_json.categories])
    return event