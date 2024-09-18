
import json
from urllib.request import urlopen
import logging

class OrisClient:
    base_url: str = "https://oris.orientacnisporty.cz/API/?format=json"
    logger = logging.getLogger(__name__)
    
    def download_entries(self, id):
        self.logger.info(f"Downloading entries for event {id}")
        method_url = f"&method=getEventEntries&eventid={id}"
        url = f"{self.base_url}{method_url}"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.logger.info(f"Entries for event {id} downloaded")
        return data_json

    def download_classes(self, id):
        self.logger.info(f"Downloading classes for event {id}")
        method_url = f"&method=getEvent&id={id}"
        url = f"{self.base_url}{method_url}"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.logger.info(f"Classes for event {id} downloaded")
        
        return data_json