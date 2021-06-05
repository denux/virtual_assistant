import requests
import pandas as pd
from dotenv import load_dotenv
import os
import geopy.distance

load_dotenv()


class FindNearest(object):
    def __init__(self, config):
        self.URL = config.get("api_url")
        self.latitude = config.get("current_lat")
        self.longitude = config.get("current_long")
        self.api_key = os.getenv("discover_api_key", "")
        self.search_limit = config.get("search_limit")
        self.talk_limit = config.get("talk_limit")

    @staticmethod
    def find_distance(lat1, lon1, lat2, lon2):
        coords_1 = (lat1, lon1)
        coords_2 = (lat2, lon2)
        return geopy.distance.great_circle(coords_1, coords_2).km

    @staticmethod
    def get_entity(command):
        return command.split("nearest ")[-1]

    def get_search_results(self, entity):
        try:
            params = {
                'apikey': self.api_key,
                'q': entity,
                'limit': self.search_limit,
                'at': '{},{}'.format(self.latitude, self.longitude)
            }

            # sending get request and saving the response as response object
            r = requests.get(url=self.URL, params=params)
            data = r.json()
            df = pd.DataFrame()
            for i in range(self.search_limit):
                title = data['items'][i]['title']
                addr = data['items'][i]['address']['label']
                lat = data['items'][i]['position']['lat']
                lng = data['items'][i]['position']['lng']
                dist = self.find_distance(lat, lng, self.latitude, self.longitude)
                df = df.append({'Title': title, 'Address': addr, 'lat': lat, 'lng': lng, 'dist': dist},
                               ignore_index=True)
            df = df.sort_values(by=['dist']).reset_index(drop=True).head(self.talk_limit)
            return df['Title'].tolist()
        except (IndexError, Exception):
            return []
