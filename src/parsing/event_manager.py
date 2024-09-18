import json


class Event_manager:
    def __init__(self):
        pass

    def add_info(self, event, event_json:dict) -> None: # get general information about event
        event_json = event_json["Data"]
        event.name = event_json["Name"]
        event.id = event_json["ID"]
        event.date = event_json["Date"]
        event.discipline = event_json["Discipline"]["ShortName"]
        event.region = event_json["Region"]
        event.organizator = event_json["Org1"]["Abbr"]
