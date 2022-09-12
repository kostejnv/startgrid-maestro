from o_startlist_creator.logic.athlete import Athlete
import json

class Entries_manager:
    def __init__(self):
        pass

    def add_athletes_info_to_cats(self, event, entries_json:json) -> None:
        entries_json = entries_json["Data"]
        for entry in entries_json.values():
            cat_name = entry['ClassDesc']
            athlete = Athlete(entry['UserID'],entry['ClubID'])
            event.categories[cat_name].athletes.append(athlete)

