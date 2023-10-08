import json


class Athlete:
    def __init__(self,id, club_id):
        self.id = id
        self.club_id = club_id

def parse_athlete(athlete_json: json) -> Athlete:
    return Athlete(athlete_json.id, athlete_json.club_id)