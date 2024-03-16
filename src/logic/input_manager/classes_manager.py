import json
from ..category import Category


class Classes_manager:
    def __init__(self):
        pass

    def get_categories(self, classes_json:json) -> dict:
        classes_json = classes_json["Data"]["Classes"]
        cats = {cat["Name"]:Category(cat["Name"]) for cat in classes_json.values()}
        return cats