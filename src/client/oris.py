
import json
from urllib.request import urlopen


class OrisClient:
    base_url: str = "https://oris.orientacnisporty.cz/API/?format=json"
    
    def download_entries(self, id):
        method_url = f"&method=getEventEntries&eventid={id}"
        url = f"{self.base_url}{method_url}"
        response = urlopen(url)
        data_json = json.loads(response.read())
        return data_json

    def download_classes(self, id):
        method_url = f"=json&method=getEvent&id={id}"
        url = f"{self.base_url}{method_url}"
        response = urlopen(url)
        data_json = json.loads(response.read())
        return data_json