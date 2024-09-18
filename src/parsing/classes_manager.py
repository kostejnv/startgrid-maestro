import json
from src.entities.category import Category


class Classes_manager:
    def __init__(self):
        pass

    def get_categories(self, classes_json:dict) -> dict:
        classes_json = classes_json["Data"]["Classes"]
        cats = {cat["Name"]:Category(cat["Name"]) for cat in classes_json.values()}
        return cats