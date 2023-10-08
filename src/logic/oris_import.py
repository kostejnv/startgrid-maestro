
import json
from urllib.request import urlopen
import os


def download_entries(id):
    url_events = f"https://oris.orientacnisporty.cz/API/?format=json&method=getEventEntries&eventid={id}"
    response = urlopen(url_events)
    data_json = json.loads(response.read())
    return data_json

def download_classes(id):
    url_events = f"https://oris.orientacnisporty.cz/API/?format=json&method=getEvent&id={id}"
    response = urlopen(url_events)
    data_json = json.loads(response.read())
    return data_json